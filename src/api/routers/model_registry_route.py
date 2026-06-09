from pathlib import Path
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status,
    BackgroundTasks
)

from src.database.connection import db_connect
from src.database.db_ops import insert_model
from src.utils.logs_handler import logger

router = APIRouter(
    prefix="/models",
    tags=["Model Registry"]
)


# def save_model_metadata(
#     model_name: str,
#     scaler_name: str,
#     metrics_name: str
# ) -> None:

#     with db_connect() as db:

#         insert_model(
#             db=db,
#             model_name=model_name,
#             scaler_name=scaler_name,
#             metrics_name=metrics_name
#         )


@router.post("/upload")
async def upload_models(
    background_tasks: BackgroundTasks,
    model_file: UploadFile = File(...),
    scaler_file: UploadFile = File(...),
    metrics_file: UploadFile = File(...)
):

    try:

        # -----------------------------
        # Filename Validation
        # -----------------------------

        model_filename = model_file.filename
        scaler_filename = scaler_file.filename
        metrics_filename = metrics_file.filename

        if not model_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model filename is missing."
            )

        if not scaler_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scaler filename is missing."
            )

        if not metrics_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Metrics filename is missing."
            )

        if not model_filename.endswith("_model.pkl"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model file must end with '_model.pkl'."
            )

        if not scaler_filename.endswith("_scaler.pkl"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scaler file must end with '_scaler.pkl'."
            )

        if not metrics_filename.endswith("_metrics.json"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Metrics file must end with '_metrics.json'."
            )

        # -----------------------------
        # Models Folder
        # -----------------------------

        project_root = Path(__file__).resolve().parents[3]

        models_dir = project_root / "models"
        metrics_dir = project_root / "metrics"

        models_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
        models_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        model_path = models_dir / model_filename
        scaler_path = models_dir / scaler_filename
        metrics_path = metrics_dir / metrics_filename

        # -----------------------------
        # Duplicate File Validation
        # -----------------------------

        if model_path.exists():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{model_filename} already exists."
            )

        if scaler_path.exists():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{scaler_filename} already exists."
            )

        if metrics_path.exists():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{metrics_filename} already exists."
            )

        # -----------------------------
        # Save Files
        # -----------------------------

        model_path.write_bytes(
            await model_file.read()
        )

        scaler_path.write_bytes(
            await scaler_file.read()
        )

        metrics_path.write_bytes(
            await metrics_file.read()
        )

        logger.info("Model files uploaded successfully")

        # -----------------------------
        # Background DB Insert
        # -----------------------------

        # background_tasks.add_task(
        #     insert_model,
        #     model_name=model_filename,
        #     scaler_name=scaler_filename,
        #     metrics_name=metrics_filename
        # )
        
        insert_model(
            model_name=model_filename,
            scaler_name=scaler_filename,
            metrics_name=metrics_filename
        )

        return {
            "status": "success",
            "message": "Model files uploaded successfully.",
            "model_name": model_filename,
            "scaler_name": scaler_filename,
            "metrics_name": metrics_filename
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Model upload failed: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload model files."
        )