from fastapi import FastAPI, Response
from .routers import prediction_route
from src.utils.logs_handler import logger
from src.models.load_models import model, scaler
from datetime import datetime

app = FastAPI(
    docs_url="/drift-docs",
    title="DriftShield",
    version="1.0.0"
)



@app.get("/health", tags=["Health Check"])
def health_check():
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
    }

# final endpoint will be /api/v1/predict
app.include_router(prediction_route.router, prefix="/api/v1")    

