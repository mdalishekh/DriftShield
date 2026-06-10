from fastapi import FastAPI, Response
from src.api.routers import model_registry_route, prediction_route
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

        if active_model:

            logger.info(
                f"Active model found: {active_model.model_name}"
            )

            try:

                load_model_into_memory(
                    model_name=active_model.model_name,
                    scaler_name=active_model.scaler_name
                )

            except FileNotFoundError as e:

                logger.warning(
                    f"Active model files not found: {e}"
                )

        else:

            logger.warning(
                "No active model found. Loading first available model."
            )

            first_model = get_first_model()

            if first_model is None:

                logger.warning(
                    "No models available in database."
                )

            else:

                try:

                    load_model_into_memory(
                        model_name=first_model.model_name,
                        scaler_name=first_model.scaler_name
                    )

                    activate_initial_model(
                        first_model.id
                    )

                except FileNotFoundError as e:

                    logger.warning(
                        f"First model files not found: {e}"
                    )

        logger.info(
            "Application startup completed"
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


# final endpoint will be /api/v1/predict
app.include_router(prediction_route.router, prefix="/api/v1")
app.include_router(model_registry_route.router, prefix="/api/v1")
