from fastapi import FastAPI
from src.api.routers import drift_route, model_registry_route, prediction_route
from src.utils.logs_handler import logger
from src.models.load_models import get_current_model
from src.database.db_ops import (
get_active_model, 
get_first_model,
activate_initial_model
)
from src.models.load_models import load_model_into_memory
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application startup initiated")

    try:

        active_model = get_active_model()

        # CASE 1 - Active model available
        if active_model is not None:

            logger.info(f"Active model found: {active_model.model_name}")

            try:
                load_model_into_memory(model_name=active_model.model_name)
                logger.info("Active model loaded successfully")

            except FileNotFoundError as e:
                logger.warning(f"Active model files not found: {e}")

            except Exception as e:
                logger.exception(f"Failed to load active model: {e}")

        
        # CASE 2 - No active model, Try first available model
        else:
            logger.warning("No active model found.")

            first_model = get_first_model()
            if first_model is not None:
                logger.info(
                    f"Loading first available model: "
                    f"{first_model.model_name}"
                )

                try:
                    load_model_into_memory(model_name=first_model.model_name)
                    
                    # Activate first model from DB
                    activate_initial_model(first_model.id)

                    logger.info(
                        f"Model {first_model.model_name} "
                        f"activated successfully"
                    )

                except FileNotFoundError as e:
                    logger.warning(f"First model files not found: {e}")

                except Exception as e:
                    logger.exception(f"Failed to load first model: {e}")

            
            # CASE 3 -  Empty Database (Application 1st boot)
            else:
                logger.warning(
                    "No models available in database. "
                    "Application will start without model."
                )
        logger.info("Application startup completed")
        yield

    except Exception as e:
        logger.exception(f"Unexpected startup error: {e}")
        yield

    finally:
        logger.info("Application shutdown initiated")


app = FastAPI(
    lifespan=lifespan,
    docs_url="/drift-docs",
    title="DriftShield",
    version="1.0.0"
)

app.mount(
    "/reports",
    StaticFiles(directory="reports"),
    name="reports"
)


# Health Check API
@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Appliation Status Check API
@app.get("/ready", tags=["Health Check"])
def readiness_check():
    model = get_current_model()

    if model is None:
        return {
            "status": "not_ready",
            "model_loaded": False
        }

    return {
        "status": "ready",
        "model_loaded": True
    }


# [ATTENTION NEEDED :- Update url and place v2]
# final endpoint will be https://{hostname}/api/v2/{routers prefix}/{endpoint}

app.include_router(prediction_route.router, prefix="/api/v1")
app.include_router(model_registry_route.router, prefix="/api/v1")
app.include_router(drift_route.router, prefix="/api/v1")

