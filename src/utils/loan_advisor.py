from logs_handler import logger


def risk_calculation(predicted_result: dict, payload: dict):
    
    risk_factors: list[dict] = []
    logger.info("Calculating risk level based on prediction result and input data")
    
    example = {
        "default": predicted_result["default"],
        "probability": predicted_result["probability"],
    }
    
    
    age = payload["age"]
    income = payload["income"]
    credit_score = payload["credit_score"]
    existing_loans = payload["existing_loans"]
    existing_loan_emi = payload["existing_loan_emi"]
    employed = payload["employed"]
    loan_amount = payload["loan_amount"]
    loan_tenure_months = payload["loan_tenure_months"]
    emi_to_income_ratio = payload["emi_to_income_ratio"]
    loan_to_income_ratio = payload["loan_to_income_ratio"]
    employment_type = payload["employment_type"]
    
    
    
    if predicted_result["default"]:
        
        # Credit score rules
        if credit_score < 600:
            risk_factors.append({"factor": "Low Credit Score", "value": credit_score})
        elif credit_score < 700:
            risk_factors.append({"factor": "Moderate Credit Score", "value": credit_score})
        elif credit_score < 750:
            risk_factors.append({"factor": "Fair Credit Score", "value": credit_score})
        else:
            risk_factors.append({"factor": "Good Credit Score", "value": credit_score})
            
        # ratio rules
        if emi_to_income_ratio > 0.5:
            risk_factors.append({"factor": "High EMI to Income Ratio", "value": emi_to_income_ratio})
        elif emi_to_income_ratio > 0.3:
            risk_factors.append({"factor": "Moderate EMI to Income Ratio", "value": emi_to_income_ratio})
        else:
            risk_factors.append({"factor": "Low EMI to Income Ratio", "value": emi_to_income_ratio})
            
            
        # loan to income ratio rules
        if loan_to_income_ratio > 7.0:
            risk_factors.append({"factor": "High Loan to Income Ratio", "value": loan_to_income_ratio})
        elif loan_to_income_ratio > 4.0:
            risk_factors.append({"factor": "Moderate Loan to Income Ratio", "value": loan_to_income_ratio})
        else:
            risk_factors.append({"factor": "Low Loan to Income Ratio", "value": loan_to_income_ratio})                    
            
    
    
    
            
# calculate emi_to_income_ratio loan_to_income_ratio
# def ratio_calculation(payload: dict):            
#     income = payload["income"]
#     existing_loan_emi = payload["existing_loan_emi"]
#     loan_amount = payload["loan_amount"]
#     loan_tenure_months = payload["loan_tenure_months"]
    
#     emi_to_income_ratio = existing_loan_emi / income if income > 0 else 0
#     loan_to_income_ratio = loan_amount / income if income > 0 else 0
    
#     return round(emi_to_income_ratio, 4), round(loan_to_income_ratio, 4)