from fastapi import (
    APIRouter,
    HTTPException,
    status
)
from src.utils.logs_handler import logger
from src.utils.drift_helper import generate_drift_report
from src.llm.llm_services import generate_drift_insights

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
    
    
@router.post("/insights")
async def get_drift_insights():

    try:


        result = generate_drift_insights()

        return {
            "status": "success",
            "message": "Drift insights generated successfully.",
            **result
        }

    except Exception as e:

        logger.exception(
            "Failed to generate drift insights"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate drift insights."
        )    