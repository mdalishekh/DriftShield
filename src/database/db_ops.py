# src/database/db_ops.py
from sqlalchemy.orm import Session
from src.database.models import Prediction
from src.database.connection import db_connect
from src.utils.logs_handler import logger

def insert_prediction(payload: dict, predicted_default: bool, probability: float):
    
    with db_connect() as db:
    
        record = Prediction(
            age=payload["age"],
            income=payload["income"],
            credit_score=payload["credit_score"],
            existing_loans=payload["existing_loans"],
            existing_loan_emi=payload["existing_loan_emi"],
            employed=payload["employed"],
            loan_amount=payload["loan_amount"],
            loan_tenure_months=payload["loan_tenure_months"],
            emi_to_income_ratio=payload["emi_to_income_ratio"],
            loan_to_income_ratio=payload["loan_to_income_ratio"],
            employment_type=payload["employment_type"],
            predicted_default=predicted_default,
            probability=probability
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


def get_all_predictions(db: Session):
    return db.query(Prediction).all()


# def save_prediction_background(
#     payload: dict,
#     result: dict
# ):
    
#     try:
#         with db_connect() as db:

#             insert_prediction(
#                 db=db,
#                 payload=payload,
#                 predicted_default=result["default"],
#                 probability=float(result["probability"])
#             )

#         logger.info(
#             "Prediction inserted into database successfully"
#         )

#     except Exception as e:

#         logger.error(
#             f"Error inserting prediction into database: {e}"
#         )