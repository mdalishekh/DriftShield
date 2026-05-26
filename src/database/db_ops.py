# src/database/db_ops.py

from sqlalchemy.orm import Session
from src.database.models import Prediction

def insert_prediction(db: Session, input_data: dict, predicted_default: bool, probability: float):
    record = Prediction(
        age=input_data["age"],
        income=input_data["income"],
        credit_score=input_data["credit_score"],
        existing_loans=input_data["existing_loans"],
        existing_loan_emi=input_data["existing_loan_emi"],
        employed=input_data["employed"],
        loan_amount=input_data["loan_amount"],
        loan_tenure_months=input_data["loan_tenure_months"],
        emi_to_income_ratio=input_data["emi_to_income_ratio"],
        loan_to_income_ratio=input_data["loan_to_income_ratio"],
        employment_type=input_data["employment_type"],
        predicted_default=predicted_default,
        probability=probability
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_predictions(db: Session):
    return db.query(Prediction).all()