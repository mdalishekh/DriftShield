from .load_models import (get_current_model, get_current_scaler)
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
    
    try:
        model = get_current_model()
        scaler = get_current_scaler()
        # Convert employed
        employed = 1 if data['employed'] == True else 0
        
        # Convert employment_type
        employment_type = EMPLOYMENT_MAP[data['employment_type']]
        
        # Prepare input
        input_df = pd.DataFrame([[
            data['age'],
            data['income'],
            data['credit_score'],
            data['existing_loans'],
            data['existing_loan_emi'],
            employed,
            data['loan_amount'],
            data['loan_tenure_months'],
            data['emi_to_income_ratio'],
            data['loan_to_income_ratio'],
            employment_type
        ]], columns=[
            'age', 'income', 'credit_score', 'existing_loans',
            'existing_loan_emi', 'employed', 'loan_amount',
            'loan_tenure_months', 'emi_to_income_ratio',
            'loan_to_income_ratio', 'employment_type'
        ])
        
        # Scale + Predict
        logger.info("Scaling input data and making prediction")
        input_scaled = scaler.transform(input_df)
        logger.info("Making prediction using the model")
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        predicted_label = True if prediction == 1 else False
        logger.info(f"Prediction made: {predicted_label}, Probability: {probability}")
        return {
            "default": predicted_label,
            "probability": round(float(probability), 4)
        }
        
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return {
            "default": False,
            "probability": 0.0
        }    
    