# New Models will be trained and deployed 
import joblib
from pathlib import Path
from src.utils.logs_handler import logger


BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "models"

# Remove .pkl from all accross Project 
# Replace it with .joblib  (Streamlit Too)

CURRENT_MODEL = None


def load_model_into_memory(model_name: str) -> None:

    global CURRENT_MODEL

    model_path = MODELS_DIR / model_name
    logger.info(f"Loading model: {model_name}")
    
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_name}"
        )
    CURRENT_MODEL = joblib.load(model_path)
    logger.info("Model loaded successfully into memory")
    
    

def get_current_model():
    # Returning Model
    return CURRENT_MODEL

