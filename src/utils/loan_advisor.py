import shap
import pandas as pd
from src.utils.logs_handler import logger
from src.models.prediction import predict_default, EMPLOYMENT_MAP
from src.models.load_models import get_current_model

# Add Exception Handler

    
def risk_calculation(predicted_result: dict, payload: dict) -> dict:
    model = get_current_model()

    if model is None:
        raise RuntimeError("No model is currently loaded.")

    input_df = pd.DataFrame([payload])

    input_df["employed"] = input_df["employed"].astype(int)
    input_df["employment_type"] = input_df["employment_type"].map(EMPLOYMENT_MAP)

    input_df = input_df[[
        "age",
        "income",
        "credit_score",
        "existing_loans",
        "existing_loan_emi",
        "employed",
        "loan_amount",
        "loan_tenure_months",
        "emi_to_income_ratio",
        "loan_to_income_ratio",
        "employment_type"
    ]]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer(input_df)

    shap_result = pd.DataFrame({
        "feature": input_df.columns,
        "value": input_df.iloc[0].values,
        "shap_value": shap_values.values[0]
    })

    shap_result["abs_shap"] = shap_result["shap_value"].abs()
    shap_result = shap_result.sort_values("abs_shap", ascending=False)

    shap_analysis = []

    for _, row in shap_result.iterrows():
        shap_analysis.append({
            "feature": row["feature"],
            "value": row["value"],
            "shap_value": round(float(row["shap_value"]), 4)
        })

    return {
        "default": predicted_result["default"],
        "probability": predicted_result["probability"],
        "shap_analysis": shap_analysis
    }    
    
    
def format_shap_analysis(shap_analysis: list[dict]) -> str:
    formatted_analysis = []

    for factor in shap_analysis:
        feature = factor["feature"]
        value = factor["value"]
        shap_value = factor["shap_value"]

        if feature in {"income", "existing_loan_emi", "loan_amount"}:
            formatted_value = f"₹ {value:,.0f}"

        elif feature == "emi_to_income_ratio":
            formatted_value = f"{value * 100:.2f}% of monthly income"

        elif feature == "loan_to_income_ratio":
            formatted_value = f"{value:.2f}x monthly income"

        elif feature == "loan_tenure_months":
            formatted_value = f"{value:.0f} months"

        else:
            formatted_value = str(value)

        formatted_analysis.append(
            f"- {feature}: {formatted_value} (SHAP: {shap_value:+.4f})"
        )
    return "\n".join(formatted_analysis)    
    
    
    
# Calculate emi_to_income_ratio loan_to_income_ratio
def ratio_calculation(payload: dict): 
    """
    Calculates EMI and loan ratios,
    updates payload in-place,
    and returns updated payload.
    """
               
    income = payload["income"]
    existing_loan_emi = payload["existing_loan_emi"]
    loan_amount = payload["loan_amount"]

    # Calculate ratios with safe division
    emi_to_income_ratio = round(existing_loan_emi / income if income > 0 else 0, 4)
    loan_to_income_ratio = round(loan_amount / income if income > 0 else 0, 4)
    
    payload.update({
        "emi_to_income_ratio": emi_to_income_ratio,
        "loan_to_income_ratio": loan_to_income_ratio
    })

    return payload


# Smart loan suggestions based on risk and positive factors
def smart_loan_suggestions(predicted_result: dict, payload: dict):

    TARGET_PROBABILITY = 0.40

    REDUCTION_FACTORS = [
        0.85,
        0.70,
        0.55,
        0.50
    ]
    
    logger.info("Starting smart loan suggestion started")

    if not predicted_result["default"]:

        logger.info("Customer already falls under acceptable risk threshold")
        return None

    requested_amount = payload["loan_amount"]
    current_tenure = payload["loan_tenure_months"]

    best_candidate = None

    # Find safe amount on current tenure

    for factor in REDUCTION_FACTORS:

        candidate_payload = payload.copy()

        candidate_amount = int(requested_amount * factor)
        candidate_payload["loan_amount"] = (candidate_amount)

        # Recalculating ratios and updating payload for candidate payload
        candidate_payload = ratio_calculation(candidate_payload)
        

        # Getting prediction for candidate payload
        prediction = predict_default(candidate_payload)
        probability = prediction["probability"]

        logger.info(
            f"Amount={candidate_amount}, "
            f"Tenure={current_tenure}, "
            f"Probability={probability}"
        )

        if probability <= TARGET_PROBABILITY:

            best_candidate = {
                "suggested_loan_amount": candidate_amount,
                "suggested_tenure": current_tenure,
                "predicted_probability":probability,
            }

            break

    if best_candidate is None:
        logger.warning("No safe loan amount found")
        return None


    # One tenure improvement check

    next_tenure = None
    # Define next tenure options based on current tenure
    if current_tenure == 12:
        next_tenure = 18
    elif current_tenure == 18:
        next_tenure = 24
    elif current_tenure == 24:
        next_tenure = 30
    elif current_tenure == 30:
        next_tenure = 36    

    if next_tenure is None:
        return best_candidate

    # Evaluate if longer tenure can further reduce risk
    candidate_payload = payload.copy()
    candidate_payload["loan_amount"] = best_candidate["suggested_loan_amount"]
    candidate_payload["loan_tenure_months"] = next_tenure
    
     # Recalculating ratios and updating payload for candidate payload with updated tenure 
    candidate_payload = ratio_calculation(candidate_payload)

    # Getting prediction for candidate payload with improved tenure
    prediction = predict_default(candidate_payload)

    improved_probability = prediction["probability"]

    if (improved_probability < best_candidate["predicted_probability"]):

        logger.info("Longer tenure produced lower risk")
        best_candidate["suggested_tenure"] = next_tenure
        best_candidate["predicted_probability"] = improved_probability

    logger.info(f"Smart suggestion generated: "f"{best_candidate}")

    return best_candidate