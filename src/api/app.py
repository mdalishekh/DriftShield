from fastapi import FastAPI, Response
from matplotlib.pylab import sample
from .routers import prediction
# from ..models.prediction import predict_default
from src.models.prediction import predict_default

app = FastAPI(docs_url="/drift-docs")



@app.get("/health")
def health_check():
    return Response(content="Application is running", media_type="text/plain")


@app.post("/predict")
def predict(data: dict):
    user = data
#     sample = {
#     "age": 56,
#     "income": 45000,
#     "credit_score": 580,
#     "existing_loans": 1,
#     "existing_loan_emi": 4500,
#     "employed": True,
#     "loan_amount": 500000,
#     "loan_tenure_months": 12,
#     "emi_to_income_ratio": 0.8,
#     "loan_to_income_ratio": 10.0,
#     "employment_type": "Salaried"
# }
    result = predict_default(data)
    return {
        "status": "success",
        "prediction": result
    }    