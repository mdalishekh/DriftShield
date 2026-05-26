from .load_models import model, scaler
import pandas as pd



EMPLOYMENT_MAP = {
    "Entrepreneur": 0,
    "Gig Worker": 1,
    "Government": 2,
    "Retired": 3,
    "Salaried": 4,
    "Self-Employed": 5
}

def predict_default(data: dict):
    
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
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]
    predicted_label = True if prediction == 1 else False
    
    return {
        "default": predicted_label,
        "probability": f"{round(float(probability) * 100, 2)}"
    }
    