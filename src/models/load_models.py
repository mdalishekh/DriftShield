# import joblib
# import json
# from pathlib import Path
# from src.utils.logs_handler import logger

# # Path setup
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# MODELS_DIR = BASE_DIR / "models"

# logger.info("Loading model and scaler from disk.")
# # Load model + scaler + metrics
# model = joblib.load(MODELS_DIR / "xgboost_model.pkl")
# scaler = joblib.load(MODELS_DIR / "scaler.pkl")
# logger.info("Model and scaler loaded successfully.")

# with open(MODELS_DIR / "baseline_metrics.json", "r") as f:
#     baseline_metrics = json.load(f)


# Export these objects for import
# __all__ = ['model', 'scaler']  #  'baseline_metrics'



import joblib
from pathlib import Path
from src.utils.logs_handler import logger


BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "models"


CURRENT_MODEL = None
CURRENT_SCALER = None


def load_model_into_memory(
    model_name: str,
    scaler_name: str
) -> None:

    global CURRENT_MODEL
    global CURRENT_SCALER

    model_path = MODELS_DIR / model_name
    scaler_path = MODELS_DIR / scaler_name

    logger.info(f"Loading model: {model_name} and scaler: {scaler_name}")

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_name}"
        )

    if not scaler_path.exists():
        raise FileNotFoundError(
            f"Scaler file not found: {scaler_name}"
        )

    
    CURRENT_MODEL = joblib.load(model_path)
    CURRENT_SCALER = joblib.load(scaler_path)

    logger.info("Model and scaler loaded successfully into memory")
    
    

def get_current_model():
    # Returning Model
    return CURRENT_MODEL


def get_current_scaler():
    # Returning Scaler
    return CURRENT_SCALER    