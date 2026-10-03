import os
from dotenv import load_dotenv

load_dotenv()

# Constant ENV variables
class ENV:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    

EXPECTED_COLUMNS = [
    "age",
    "income",
    "credit_score",
    "existing_loans",
    "existing_loan_emi",
    "employed",
    "default",
    "loan_amount",
    "loan_tenure_months",
    "emi_to_income_ratio",
    "loan_to_income_ratio",
    "employment_type"
]

EXPECTED_FEATURES = [
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
]