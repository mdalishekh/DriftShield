from src.utils.logs_handler import logger
from src.models.prediction import predict_default

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
def ratio_calculation(payload: dict):            
    income = payload["income"]
    existing_loan_emi = payload["existing_loan_emi"]
    loan_amount = payload["loan_amount"]

    emi_to_income_ratio = existing_loan_emi / income if income > 0 else 0
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    
    return round(emi_to_income_ratio, 4), round(loan_to_income_ratio, 4)






# Smart loan suggestions based on risk and positive factors



TARGET_PROBABILITY = 0.40

REDUCTION_FACTORS = [
    0.85,
    0.70,
    0.55,
    0.50
]


def smart_loan_suggestions(
    predicted_result: dict,
    payload: dict
):

    logger.info(
        "Starting smart loan suggestion process"
    )

    if not predicted_result["default"]:

        logger.info(
            "Customer already falls under acceptable risk threshold"
        )

        return None

    requested_amount = payload["loan_amount"]
    current_tenure = payload["loan_tenure_months"]

    best_candidate = None

    # ------------------------------
    # STEP 1
    # Find safe amount on current tenure
    # ------------------------------

    for factor in REDUCTION_FACTORS:

        candidate_payload = payload.copy()

        candidate_amount = int(
            requested_amount * factor
        )

        candidate_payload["loan_amount"] = (
            candidate_amount
        )

        emi_ratio, loan_ratio = (
            ratio_calculation(
                candidate_payload
            )
        )

        candidate_payload[
            "emi_to_income_ratio"
        ] = emi_ratio

        candidate_payload["loan_to_income_ratio"] = loan_ratio

        prediction = predict_default(candidate_payload)

        probability = prediction["probability"]

        logger.info(
            f"Amount={candidate_amount}, "
            f"Tenure={current_tenure}, "
            f"Probability={probability}"
        )

        if probability <= TARGET_PROBABILITY:

            best_candidate = {
                "suggested_loan_amount":
                    candidate_amount,

                "suggested_tenure":
                    current_tenure,

                "predicted_probability":
                    probability,
            }

            break

    if best_candidate is None:

        logger.warning(
            "No safe loan amount found"
        )

        return None

    # ------------------------------
    # STEP 2
    # One tenure improvement check
    # ------------------------------

    next_tenure = None

    if current_tenure == 12:
        next_tenure = 24

    elif current_tenure == 18:
        next_tenure = 30

    elif current_tenure == 24:
        next_tenure = 36

    if next_tenure is None:

        return best_candidate

    candidate_payload = payload.copy()

    candidate_payload["loan_amount"] = (
        best_candidate[
            "suggested_loan_amount"
        ]
    )

    candidate_payload["loan_tenure_months"] = (
        next_tenure
    )

    emi_ratio, loan_ratio = (
        ratio_calculation(
            candidate_payload
        )
    )

    candidate_payload[
        "emi_to_income_ratio"
    ] = emi_ratio

    candidate_payload[
        "loan_to_income_ratio"
    ] = loan_ratio

    prediction = predict_default(
        candidate_payload
    )

    improved_probability = prediction[
        "probability"
    ]

    if (
        improved_probability
        < best_candidate[
            "predicted_probability"
        ]
    ):

        logger.info("Longer tenure produced lower risk")

        best_candidate[
            "suggested_tenure"
        ] = next_tenure

        best_candidate[
            "predicted_probability"
        ] = improved_probability

    logger.info(
        f"Smart suggestion generated: "
        f"{best_candidate}"
    )

    return best_candidate