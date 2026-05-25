from fastapi import APIRouter, Response
from src.models.prediction import predict_default
from src.utils.logs_handler import logger

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/")
def predict(data: dict):
    logger.info("Prediction request recieved")
    result = predict_default(data)
    logger.info(f"Prediction result: {result}")
    return {
        "status": "success",
        "prediction": result
    }    