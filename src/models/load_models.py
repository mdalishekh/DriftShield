import joblib
import json
from pathlib import Path
from src.utils.logs_handler import logger

# Path setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"

logger.info("Loading model and scaler from disk.")
# Load model + scaler + metrics
model = joblib.load(MODELS_DIR / "xgboost_model.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
logger.info("Model and scaler loaded successfully.")

# with open(MODELS_DIR / "baseline_metrics.json", "r") as f:
#     baseline_metrics = json.load(f)


# Export these objects for import
# __all__ = ['model', 'scaler']  #  'baseline_metrics'

