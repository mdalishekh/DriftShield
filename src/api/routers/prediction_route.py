from fastapi import APIRouter, Response
from src.models.prediction import predict_default
from src.utils.logs_handler import logger
from src.api.schemas.schema import PredictionRequest, PredictionResponse
from src.database.connection import db_connect
from src.database.db_ops import insert_prediction

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    logger.info("Prediction request received")
    result = predict_default(data.model_dump())
    logger.info(f"Prediction result: {result}")
    with db_connect() as db:
        logger.info("Inserting prediction into database")
        insert_prediction(
            db=db,
            input_data=data.model_dump(),
            predicted_default=result["default"],
            probability= float(result["probability"])
        )
        logger.info("Prediction inserted into database successfully")
    return PredictionResponse(
        status="success",
        prediction=result # type: ignore
    )