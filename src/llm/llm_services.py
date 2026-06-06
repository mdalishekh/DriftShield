from src.utils.logs_handler import logger
from src.utils.loan_advisor import risk_calculation
from src.llm.prompts import (loan_advisor_prompt, LOAN_ADVISOR_CONTEXT)
from src.llm.groq_client import GroqClient




def generate_loan_assessment(predicted_result: dict, payload: dict) -> str:

    logger.info("Generating loan assessment using LLM")

    # Step 1: Calculate risk and positive factors
    analysis_result = risk_calculation(predicted_result, payload)

    # Step 2: Create prompt for LLM
    # system_prompt = LOAN_ADVISOR_CONTEXT
    
    user_prompt = loan_advisor_prompt(
        default=predicted_result["default"],
        probability=float(predicted_result["probability"]) , # / 100
        risk_factors=analysis_result["risk_factors"],
        positive_factors=analysis_result["positive_factors"]
    )

    # Step 3: Generate response from LLM
    groq_client = GroqClient()
    assessment = groq_client.generate_response(
        system_prompt=LOAN_ADVISOR_CONTEXT,
        user_prompt=user_prompt,
    )

    return assessment