from fastapi import APIRouter, BackgroundTasks
from src.models.prediction import predict_default
from src.utils.logs_handler import logger
from src.api.schemas.schema import PredictionRequest, PredictionResponse
from src.database.connection import db_connect
from src.database.db_ops import insert_prediction
from src.llm.llm_services import generate_loan_assessment
from src.utils.loan_advisor import ratio_calculation

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest, background_tasks: BackgroundTasks):
    logger.info("Prediction request received")
    
    input_data:dict = data.model_dump()
    
    # Calculating ratios and updating payload dic
    payload: dict = ratio_calculation(input_data)
    
    # Get prediction result from the model
    result = predict_default(payload)
    
    # generate LLM response for loan assessment  
    try:    
        llm_response = generate_loan_assessment(result, payload)   
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        llm_response = "Could not generate loan assessment at this time."
    
   # Start DB insertion in background
    background_tasks.add_task(
    insert_prediction,
    payload.copy(),
    result["default"],
    float(result["probability"])
    )  
  
    # Convert probability to percentage and round to 2 decimal places         
    result.update({"probability": round(float(result["probability"]*100), 2)})

    return PredictionResponse(
        status="success",
        prediction=result, # type: ignore
        llm_response=llm_response
    )