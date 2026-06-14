from pathlib import Path
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status
)


from src.utils.logs_handler import logger
from src.utils.drift_helper import generate_drift_report

router = APIRouter(
    prefix="/drift",
    tags=["Drift Detection"]
)


@router.post("/report")
def generate_report():
    logger.info("Drift Detection requested")
    result = generate_drift_report()

    return {
        "status": "success",
        "message": "Drift report generated successfully.",
        "html_file" : result["html_file"],
        "json_file": result["json_file"],
        "reference_csv_file" : result["reference_csv_file"]
    }