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
    # Output default
    predicted_default = Column(Boolean, nullable=False)
    loan_amount = Column(Integer, nullable=False)
    loan_tenure_months = Column(Integer, nullable=False)
    emi_to_income_ratio = Column(Float, nullable=False)
    loan_to_income_ratio = Column(Float, nullable=False)
    employment_type = Column(String, nullable=False)
    
    # Output
    probability = Column(Float, nullable=False)
    # Meta
    timestamp = Column(DateTime, default=datetime.now)
    
    
    
class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True,autoincrement=True)

    # Input Features
    model_name = Column(String, nullable=False, unique=True)
    scaler_name = Column(String,nullable=False,unique=True)
    metrics_name = Column(String, nullable=False, unique=True)
    reference_csv_name = Column(String, nullable=False, unique=True)
    uploaded_at = Column(DateTime, default=datetime.now, nullable=False)
    activated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)    