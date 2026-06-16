from pathlib import Path
from src.utils.logs_handler import logger
from src.utils.loan_advisor import risk_calculation
from src.llm.prompts import (
    loan_advisor_prompt, 
    build_drift_prompt, 
    DRIFT_CONTEXT,
    LOAN_ADVISOR_CONTEXT
    )
from src.utils.loan_advisor import smart_loan_suggestions
from src.llm.groq_client import GroqClient
from src.utils.drift_helper import parse_drift_metrics

groq_client = GroqClient()

def generate_loan_assessment(predicted_result: dict, payload: dict) -> str:

    logger.info("Generating loan assessment using LLM")

    # Calculate risk and positive factors
    analysis_result = risk_calculation(predicted_result, payload)
    
    # Generate smart loan suggestions based on risk and positive factors
    loan_suggestion = smart_loan_suggestions(predicted_result, payload)
    
    # Creating user prompt for LLM with all the necessary information
    user_prompt = loan_advisor_prompt(
        default=predicted_result["default"],
        probability=round(float(predicted_result["probability"])*100, 2),
        risk_factors=analysis_result["risk_factors"],
        positive_factors=analysis_result["positive_factors"],
        loan_suggestion=loan_suggestion
    )

    # Generate response from LLM
    
    assessment = groq_client.generate_response(
        system_prompt=LOAN_ADVISOR_CONTEXT,
        user_prompt=user_prompt,
        max_tokens=500
    )

    return assessment




def generate_drift_insights():
    
    project_root = Path(__file__).resolve().parents[2]

    json_path = (
        project_root
        / "metrics"
        / "drift_metrics.json"
    )

    parsed_metrics = parse_drift_metrics(json_path)

    user_prompt = build_drift_prompt(parsed_metrics)

    llm_response = groq_client.generate_response(
        system_prompt=DRIFT_CONTEXT,
        user_prompt=user_prompt,
        max_tokens=500
    )

    return {
        "drift_status": parsed_metrics["status"],
        "drift_percentage": parsed_metrics["drift_percentage"],
        "llm_response": llm_response
    }