# New Models are expected to be uploaded

from pathlib import Path
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status
)

from src.database.db_ops import (
    insert_model_metadata, 
    get_all_models,
    get_model_by_id,
    delete_model_record,
    get_active_model,
    switch_active_model,
    get_first_model,
    activate_initial_model
    )
from src.models.load_models import load_model_into_memory
from src.utils.logs_handler import logger

router = APIRouter(
    prefix="/models",
    tags=["Model Registry"]
)


# Exception handling and status code to be added very soon

# Uploading New Models into the application - API
@router.post("/upload")
async def upload_models(
    model_file: UploadFile = File(...),
    metrics_file: UploadFile = File(...),
    reference_csv: UploadFile = File(...)
):
    try:
        # Validate filenames
        model_filename = model_file.filename
        metrics_filename = metrics_file.filename
        reference_csv_filename = reference_csv.filename

        if not model_filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Model file is missing.")

        if not metrics_filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Metrics file is missing.")

        if not reference_csv_filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reference CSV file is missing.")

        # Checking file naming convention
        if not model_filename.endswith("_model.json"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Model file must end with '_model.json'.")

        if not metrics_filename.endswith("_metrics.json"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Metrics file must end with '_metrics.json'.")

        if not reference_csv_filename.endswith("_reference.csv"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Reference CSV file must end with '_reference.csv'.")

        # Prepare directories and file paths
        parent_dir = Path(__file__).resolve().parents[3]

        models_dir = parent_dir / "models"
        metrics_dir = parent_dir / "metrics"
        reference_dir = parent_dir / "csv"

        models_dir.mkdir(parents=True, exist_ok=True)
        metrics_dir.mkdir(parents=True, exist_ok=True)
        reference_dir.mkdir(parents=True, exist_ok=True)

        model_path = models_dir / model_filename
        metrics_path = metrics_dir / metrics_filename
        reference_path = reference_dir / reference_csv_filename

        # Prevent duplicate files
        if model_path.exists():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"{model_filename} already exists.")

        if metrics_path.exists():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"{metrics_filename} already exists.")

        if reference_path.exists():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"{reference_csv_filename} already exists.")

        # Determine whether this is the first model
        is_first_model = get_first_model() is None

        # Save uploaded files
        logger.info("Uploading model, metrics and reference CSV files")

        model_path.write_bytes(await model_file.read())
        metrics_path.write_bytes(await metrics_file.read())
        reference_path.write_bytes(await reference_csv.read())

        logger.info("Model, metrics and reference CSV files uploaded successfully")

        # Register model metadata
        new_model = insert_model_metadata(
            model_name=model_filename,
            metrics_name=metrics_filename,
            reference_csv_name=reference_csv_filename
        )

        # Automatically activate the first uploaded model
        if is_first_model:
            try:
                load_model_into_memory(model_name=new_model.model_name)
                activate_initial_model(new_model.id)
                logger.info(f"Model {new_model.model_name} activated successfully")

            except FileNotFoundError as e:
                logger.warning(f"First model files not found: {e}")

            except Exception:
                logger.exception(f"Failed to load first model: {new_model.model_name}")

        return {
            "status": "success",
            "message": "Model files uploaded successfully.",
            "model_name": model_filename,
            "metrics_name": metrics_filename,
            "reference_csv_name": reference_csv_filename
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Model & Metrics upload failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload model files."
        )
        
        
# Getting list of all Model - API
@router.get("/list")
def get_models():

    logger.info("Fetching all registered models")

    try:
        # Getting all available models
        models = get_all_models()

        return {
            "status": "success",
            "models": [
                {
                    "id": model.id,
                    "model_name": model.model_name,
                    "metrics_name": model.metrics_name,
                    "reference_csv_name": model.reference_csv_name,
                    "uploaded_at": model.uploaded_at,
                    "activated_at": model.activated_at,
                    "is_active": model.is_active
                }
                for model in models
            ]
        }

    except Exception:
        logger.exception("Failed to fetch registered models")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch registered models."
        )        
        

# Deleting any specific Model - API
@router.delete("/delete/{model_id}")
def delete_model(model_id: int):

    logger.info(f"Delete request received for model ID: {model_id}")

    try:
        # Getting model details
        model_record = get_model_by_id(model_id)

        if model_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No model found for ID {model_id}"
            )

        if model_record.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active model cannot be deleted."
            )

        project_root = Path(__file__).resolve().parents[3]
        model_path = (project_root/"models"/model_record.model_name)
        metrics_path = (project_root/"metrics"/model_record.metrics_name)
        reference_csv_path = (project_root/"csv"/model_record.reference_csv_name)

        model_path.unlink()
        metrics_path.unlink()
        reference_csv_path.unlink()

        logger.info(f"Files deleted successfully for model ID: {model_id}")

        # Deleting specific Model by it's ID
        delete_model_record(model_id)

        return {
            "status": "success",
            "message": "Model deleted successfully.",
            "deleted_record": {
                "id": model_record.id,
                "model_name": model_record.model_name,
                "metrics_name": model_record.metrics_name,
                "uploaded_at": model_record.uploaded_at,
                "activated_at": model_record.activated_at,
                "is_active": model_record.is_active
            }
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception(f"Failed to delete model ID: {model_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete model."
        )
        
        
# Activating any specific Model - API     
@router.put("/activate/{model_id}")
def activate_model(model_id: int):

    logger.info(f"Activation request received for model ID: {model_id}")

    try:
        # Getting model details
        model_record = get_model_by_id(model_id)

        if model_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No model found for ID {model_id}"
            )

        if model_record.is_active:
            return {
                "status": "warning",
                "message": "Selected model is already active."
            }

        # Loads new model into application's Memory
        load_model_into_memory(model_name=model_record.model_name)

        # Getting currently loaded model details
        current_active_model = get_active_model()

        # Updates model status in database
        switch_active_model(
            current_active_id=current_active_model.id,
            new_active_id=model_record.id
        )

        logger.info(f"Model activated successfully. ID: {model_id}")

        return {
            "status": "success",
            "message": "Model activated successfully.",
            "model_id": model_record.id,
            "model_name": model_record.model_name,
            "reference_csv_name": model_record.reference_csv_name
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception(f"Failed to activate model ID: {model_id}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate model."
        )        

# Not in use for now
@router.post("/data-pipeline")
def data_processing_pipeline():
    return None 
