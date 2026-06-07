from fastapi import APIRouter, Response
from src.models.prediction import predict_default
from src.utils.logs_handler import logger
from src.api.schemas.schema import PredictionRequest, PredictionResponse
from src.database.connection import db_connect
from src.database.db_ops import insert_prediction
from src.llm.llm_services import generate_loan_assessment
from src.utils.loan_advisor import ratio_calculation

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    logger.info("Prediction request received")
    
    payload = data.model_dump()

    emi_ratio, loan_ratio = ratio_calculation(payload)
    
    payload.update({
        "emi_to_income_ratio": emi_ratio,
        "loan_to_income_ratio": loan_ratio
    })

    result = predict_default(payload)
    
    logger.info(f"Prediction result: {result}")
    
    with db_connect() as db:
        logger.info("Inserting prediction into database")
        insert_prediction(
            db=db,
            input_data=payload,
            predicted_default=result["default"],
            probability= float(result["probability"])
        )
        
        logger.info("Prediction inserted into database successfully")
        
    llm_response = generate_loan_assessment(result, payload)    
    result.update({"proabability": float(result["probability"]*100)})
    return PredictionResponse(
        status="success",
        prediction=result, # type: ignore
        response=llm_response
    )