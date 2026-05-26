# src/database/models.py

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Input features
    age = Column(Integer, nullable=False)
    income = Column(Integer, nullable=False)
    credit_score = Column(Integer, nullable=False)
    existing_loans = Column(Integer, nullable=False)
    existing_loan_emi = Column(Integer, nullable=False)
    employed = Column(Boolean, nullable=False)
    loan_amount = Column(Integer, nullable=False)
    loan_tenure_months = Column(Integer, nullable=False)
    emi_to_income_ratio = Column(Float, nullable=False)
    loan_to_income_ratio = Column(Float, nullable=False)
    employment_type = Column(String, nullable=False)
    # Output
    predicted_default = Column(Boolean, nullable=False)
    probability = Column(Float, nullable=False)
    # Meta
    timestamp = Column(DateTime, default=datetime.now)