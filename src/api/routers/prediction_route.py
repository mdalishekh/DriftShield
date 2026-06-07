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

    # Get prediction result from the model
    result = predict_default(payload)
        
    # Datebase connection and insertion
    with db_connect() as db:
        logger.info("Inserting prediction into database")
        
        try:
            insert_prediction(
                db=db,
                input_data=payload,
                predicted_default=result["default"],
                probability= float(result["probability"])
            )
            logger.info("Prediction inserted into database successfully")
        except Exception as e:
            logger.error(f"Error inserting prediction into database: {e}")
        
    # generate LLM response for loan assessment    
    try:    
        llm_response = generate_loan_assessment(result, payload)   
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        llm_response = "Could not generate loan assessment at this time."
    
    # Convert probability to percentage and round to 2 decimal places         
    result.update({"probability": round(float(result["probability"]*100), 2)})
    
    return PredictionResponse(
        status="success",
        prediction=result, # type: ignore
        llm_response=llm_response
    )