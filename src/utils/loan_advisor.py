from src.utils.logs_handler import logger


def risk_calculation(predicted_result: dict, payload: dict) -> dict:

    logger.info(
        "Calculating risk and positive factors based on prediction result and input data"
    )

    risk_factors: list[dict] = []
    positive_factors: list[dict] = []

    credit_score = payload["credit_score"]
    income = payload["income"]
    existing_loans = payload["existing_loans"]
    employed = payload["employed"]
    employment_type = payload["employment_type"]

    emi_to_income_ratio = payload["emi_to_income_ratio"]
    loan_to_income_ratio = payload["loan_to_income_ratio"]

    # ==================================
    # Credit Score Analysis
    # ==================================

    if credit_score < 600:
        risk_factors.append(
            {
                "factor": "Low Credit Score",
                "value": credit_score,
            }
        )

    elif credit_score < 700:
        risk_factors.append(
            {
                "factor": "Moderate Credit Score",
                "value": credit_score,
            }
        )

    elif credit_score >= 750:
        positive_factors.append(
            {
                "factor": "Strong Credit Profile",
                "value": credit_score,
            }
        )

    # ==================================
    # EMI Burden Analysis
    # ==================================

    if emi_to_income_ratio >= 0.45:
        risk_factors.append(
            {
                "factor": "High EMI Burden",
                "value": round(emi_to_income_ratio, 4),
            }
        )

    elif emi_to_income_ratio >= 0.30:
        risk_factors.append(
            {
                "factor": "Moderate EMI Burden",
                "value": round(emi_to_income_ratio, 4),
            }
        )

    else:
        positive_factors.append(
            {
                "factor": "Manageable EMI Burden",
                "value": round(emi_to_income_ratio, 4),
            }
        )

    # ==================================
    # Loan To Income Ratio Analysis
    # ==================================

    if loan_to_income_ratio >= 7:
        risk_factors.append(
            {
                "factor": "High Loan-To-Income Ratio",
                "value": round(loan_to_income_ratio, 4),
            }
        )

    elif loan_to_income_ratio >= 5:
        risk_factors.append(
            {
                "factor": "Moderate Loan-To-Income Ratio",
                "value": round(loan_to_income_ratio, 4),
            }
        )

    else:
        positive_factors.append(
            {
                "factor": "Healthy Loan-To-Income Ratio",
                "value": round(loan_to_income_ratio, 4),
            }
        )

    # ==================================
    # Existing Loans Analysis
    # ==================================

    if existing_loans >= 4:
        risk_factors.append(
            {
                "factor": "Multiple Existing Loans",
                "value": existing_loans,
            }
        )

    elif existing_loans <= 1:
        positive_factors.append(
            {
                "factor": "Limited Existing Debt Obligations",
                "value": existing_loans,
            }
        )

    # ==================================
    # Employment Status Analysis
    # ==================================

    if not employed:
        risk_factors.append(
            {
                "factor": "No Active Employment",
                "value": employed,
            }
        )

    else:
        positive_factors.append(
            {
                "factor": "Active Employment",
                "value": employed,
            }
        )

    # ==================================
    # Employment Stability Analysis
    # ==================================

    if (
        employment_type == "Gig Worker"
        and income < 25000
    ):
        risk_factors.append(
            {
                "factor": "Variable Income Stability",
                "value": {
                    "employment_type": employment_type,
                    "income": income,
                },
            }
        )

    elif (
        employment_type == "Self-Employed"
        and income < 60000
    ):
        risk_factors.append(
            {
                "factor": "Variable Income Stability",
                "value": {
                    "employment_type": employment_type,
                    "income": income,
                },
            }
        )

    # ==================================
    # Positive Employment Profiles
    # ==================================

    if employment_type == "Government":
        positive_factors.append(
            {
                "factor": "Stable Employment Profile",
                "value": employment_type,
            }
        )

    elif employment_type == "Salaried":
        positive_factors.append(
            {
                "factor": "Consistent Income Source",
                "value": employment_type,
            }
        )

    logger.info(
        f"\n\nRisk factors identified: {len(risk_factors)}, "
        f"Positive factors identified: {len(positive_factors)}\n\n"
    )

    return {
        "default": predicted_result["default"],
        "probability": predicted_result["probability"],
        "risk_factors": risk_factors,
        "positive_factors": positive_factors,
    }
    
            
# calculate emi_to_income_ratio loan_to_income_ratio
# def ratio_calculation(payload: dict):            
#     income = payload["income"]
#     existing_loan_emi = payload["existing_loan_emi"]
#     loan_amount = payload["loan_amount"]
#     loan_tenure_months = payload["loan_tenure_months"]
    
#     emi_to_income_ratio = existing_loan_emi / income if income > 0 else 0
#     loan_to_income_ratio = loan_amount / income if income > 0 else 0
    
#     return round(emi_to_income_ratio, 4), round(loan_to_income_ratio, 4)