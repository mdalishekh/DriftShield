from pydantic import BaseModel, Field
from typing import Literal

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: int = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=900)
    existing_loans: int = Field(..., ge=0)
    existing_loan_emi: int = Field(..., ge=0)
    employed: bool
    loan_amount: int = Field(..., gt=0)
    loan_tenure_months: int = Field(..., gt=0)
    emi_to_income_ratio: float = Field(..., ge=0)
    loan_to_income_ratio: float = Field(..., ge=0)
    employment_type: Literal[
        "Entrepreneur", "Gig Worker", "Government",
        "Retired", "Salaried", "Self-Employed"
    ]

class PredictionData(BaseModel):
    default: bool
    probability: float

class PredictionResponse(BaseModel):
    status: str
    prediction: PredictionData
    response: str