from .load_models import get_current_model
import pandas as pd
from src.utils.logs_handler import logger


EMPLOYMENT_MAP = {
    "Entrepreneur": 0,
    "Gig Worker": 1,
    "Government": 2,
    "Retired": 3,
    "Salaried": 4,
    "Self-Employed": 5
}


def predict_default(data: dict):
    model = get_current_model()

    if model is None:
        raise RuntimeError("No model is currently loaded.")

    employed = 1 if data["employed"] else 0
    employment_type = EMPLOYMENT_MAP[data["employment_type"]]

    input_df = pd.DataFrame([[
        data["age"],
        data["income"],
        data["credit_score"],
        data["existing_loans"],
        data["existing_loan_emi"],
        employed,
        data["loan_amount"],
        data["loan_tenure_months"],
        data["emi_to_income_ratio"],
        data["loan_to_income_ratio"],
        employment_type
    ]], columns=[
        "age", "income", "credit_score", "existing_loans",
        "existing_loan_emi", "employed", "loan_amount",
        "loan_tenure_months", "emi_to_income_ratio",
        "loan_to_income_ratio", "employment_type"
    ])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return {
        "default": bool(prediction == 1),
        "probability": round(float(probability), 4)
    }