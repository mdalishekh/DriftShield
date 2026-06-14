from fastapi import FastAPI
from src.api.routers import drift_route, model_registry_route, prediction_route
from src.utils.logs_handler import logger
from src.models.load_models import (get_current_model, get_current_scaler)
from src.database.db_ops import (
    get_active_model, 
    get_first_model,
    activate_initial_model
    )
from src.models.load_models import load_model_into_memory
from contextlib import asynccontextmanager
from datetime import datetime



@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application startup initiated")

    try:

        active_model = get_active_model()

        # --------------------------------------------------
        # CASE 1
        # Active model available
        # --------------------------------------------------
        if active_model is not None:

            logger.info(
                f"Active model found: {active_model.model_name}"
            )

            try:

                load_model_into_memory(
                    model_name=active_model.model_name,
                    scaler_name=active_model.scaler_name
                )

                logger.info(
                    "Active model loaded successfully"
                )

            except FileNotFoundError as e:

                logger.warning(
                    f"Active model files not found: {e}"
                )

            except Exception as e:

                logger.error(
                    f"Failed to load active model: {e}"
                )

        # --------------------------------------------------
        # CASE 2
        # No active model
        # Try first available model
        # --------------------------------------------------
        else:

            logger.warning(
                "No active model found."
            )

            first_model = get_first_model()

            if first_model is not None:

                logger.info(
                    f"Loading first available model: "
                    f"{first_model.model_name}"
                )

                try:

                    load_model_into_memory(
                        model_name=first_model.model_name,
                        scaler_name=first_model.scaler_name
                    )

                    activate_initial_model(
                        first_model.id
                    )

                    logger.info(
                        f"Model {first_model.model_name} "
                        f"activated successfully"
                    )

                except FileNotFoundError as e:

                    logger.warning(
                        f"First model files not found: {e}"
                    )

                except Exception as e:

                    logger.error(
                        f"Failed to load first model: {e}"
                    )

            # --------------------------------------------------
            # CASE 3
            # Empty Database
            # --------------------------------------------------
            else:

                logger.warning(
                    "No models available in database. "
                    "Application will start without model."
                )

        logger.info(
            "Application startup completed"
        )

        yield

    except Exception as e:

        logger.error(
            f"Unexpected startup error: {e}"
        )

        yield

    finally:

        logger.info(
            "Application shutdown initiated"
        )


app = FastAPI(
    lifespan=lifespan,
    docs_url="/drift-docs",
    title="DriftShield",
    version="1.0.0"
)



@app.get("/health", tags=["Health Check"])
def health_check():
    logger.info("Health check requested")
    model = get_current_model()
    scaler = get_current_scaler()
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
    }


# final endpoint will be /api/v1/{routers prefix}/{endpoint}
app.include_router(prediction_route.router, prefix="/api/v1")
app.include_router(model_registry_route.router, prefix="/api/v1")
app.include_router(drift_route.router, prefix="/api/v1")

