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

# Generating Drift report using Evidently
@router.post("/report")
def generate_report():
    logger.info("Drift Detection requested")

    try:
        result = generate_drift_report()

        return {
            "status": "success",
            "message": "Drift report generated successfully.",
            "html_file": result["html_file"],
            "json_file": result["json_file"],
            "reference_csv_file": result["reference_csv_file"]
        }

    except ValueError as e:
        logger.warning(f"Drift report validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except FileNotFoundError as e:
        logger.error(f"Drift report file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception:
        logger.exception("Failed to generate drift report")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate drift report."
        )
    
  
# Generating LLM Insight using Evidently JSON Report    
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
