from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from src.models.prediction import predict_default
from src.utils.logs_handler import logger
from src.api.schemas.schema import PredictionRequest, PredictionResponse
from src.database.db_ops import insert_prediction
from src.llm.llm_services import generate_loan_assessment
from src.utils.loan_advisor import ratio_calculation


router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest, background_tasks: BackgroundTasks):
    try:
        logger.info("Prediction request received")

        input_data: dict = data.model_dump()
        payload: dict = ratio_calculation(input_data)

        result = predict_default(payload)

        try:
            llm_response = generate_loan_assessment(result, payload)
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            llm_response = "Could not generate loan assessment at this time."

        background_tasks.add_task(
            insert_prediction,
            payload.copy(),
            result["default"],
            float(result["probability"])
        )

        prediction = {
            "default": result["default"],
            "probability": round(float(result["probability"]) * 100, 2)
        }

        return PredictionResponse(
            status="success",
            prediction=prediction, # type: ignore
            llm_response=llm_response
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    except Exception:
        logger.exception("Prediction request failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process prediction request."
        )