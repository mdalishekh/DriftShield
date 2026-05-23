import joblib
import json
from pathlib import Path

# Path setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"

print("Loading model and scaler...")
# Load model + scaler + metrics
model = joblib.load(MODELS_DIR / "xgboost_model.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
print("Model and scaler loaded successfully.")
# with open(MODELS_DIR / "baseline_metrics.json", "r") as f:
#     baseline_metrics = json.load(f)

# Export these objects for import
# __all__ = ['model', 'scaler']  #  'baseline_metrics'

