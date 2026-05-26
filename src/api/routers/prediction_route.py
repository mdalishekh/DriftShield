from fastapi import APIRouter, Response
from src.models.prediction import predict_default
from src.utils.logs_handler import logger
from src.api.schemas.schema import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    logger.info("Prediction request received")
    result = predict_default(data.model_dump())
    logger.info(f"Prediction result: {result}")
    return PredictionResponse(
        status="success",
        prediction=result
    )