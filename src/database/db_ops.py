# src/database/db_ops.py
from sqlalchemy.orm import Session
from src.database.models import Prediction, ModelRegistry
from src.database.connection import db_connect
from src.utils.logs_handler import logger
from datetime import datetime


# This function inserts Incoming user data in database
def insert_prediction(payload: dict, predicted_default: bool, probability: float):
    
    # Connecting with Database
    with db_connect() as db:
    
        record = Prediction(
            age=payload["age"],
            income=payload["income"],
            credit_score=payload["credit_score"],
            existing_loans=payload["existing_loans"],
            existing_loan_emi=payload["existing_loan_emi"],
            employed=payload["employed"],
            loan_amount=payload["loan_amount"],
            loan_tenure_months=payload["loan_tenure_months"],
            emi_to_income_ratio=payload["emi_to_income_ratio"],
            loan_to_income_ratio=payload["loan_to_income_ratio"],
            employment_type=payload["employment_type"],
            default=predicted_default,
            probability=probability
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


def get_all_predictions(db: Session):
    return db.query(Prediction).all()


# This functions insets Model & Metrics file's metadata in Database
def insert_model_metadata(**kwargs)-> ModelRegistry:
    
    # Connecting with Database
    with db_connect() as db:
        logger.info("Inserting Model & Metrics metadata")
        try:
            model_record = ModelRegistry(**kwargs)
            db.add(model_record)
            db.commit()
            db.refresh(model_record)
            logger.info("Model & Metrics metadata inserted successfully")
            return model_record

        except Exception as e:
            logger.exception("Failed to insert Model & Metric metadata")
            db.rollback()
            raise
        
        

# This functions fetch record corresponding to the provided Row ID
def get_model_by_id(model_id: int) -> ModelRegistry | None:

    with db_connect() as db:

        logger.info(f"Fetching record details for ID: {model_id}")

        try:

            model_record = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.id == model_id)
                .first()
            )

            if model_record:
                logger.info(f"Record found for ID: {model_id}")
                return model_record

            logger.warning(f"Record does not exist for ID: {model_id}")
            return None

        except Exception:
            logger.exception(f"Failed to fetch record details for ID: {model_id}")
            raise        
        


# This function extract all models record from database 
def get_all_models() -> list[ModelRegistry]:

    with db_connect() as db:

        logger.info("Fetching all registered models")

        try:

            models = db.query(ModelRegistry).all()

            logger.info(f"Successfully fetched {len(models)} model records")

            return models

        except Exception:
            logger.exception("Failed to fetch model records")
            raise        
        
        


def delete_model_record(model_id: int) -> None:

    with db_connect() as db:

        logger.info(f"Deleting model record for ID: {model_id}")

        try:

            model_record = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.id == model_id)
                .first()
            )

            if model_record is None:
                logger.warning(f"No model record found for ID: {model_id}")
                return

            db.delete(model_record)
            db.commit()

            logger.info(f"Model record deleted successfully for ID: {model_id}")

        except Exception:
            db.rollback()
            logger.exception(f"Failed to delete model record for ID: {model_id}")
            raise        
        
        

def get_active_model() -> ModelRegistry | None:

    with db_connect() as db:

        logger.info("Fetching active model")

        try:

            active_model = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.is_active == True)
                .first()
            )

            if active_model:
                logger.info(f"Active model found: {active_model.model_name}")
                return active_model

            logger.warning("No active model found in database")

            return None

        except Exception:
            logger.exception("Failed to fetch active model")
            raise        
        
        



def switch_active_model(
    current_active_id: int,
    new_active_id: int
) -> None:

    with db_connect() as db:

        logger.info(f"Switching active model from ID {current_active_id} to ID {new_active_id}")

        try:

            current_active_model = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.id == current_active_id)
                .first()
            )

            new_active_model = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.id == new_active_id)
                .first()
            )

            if current_active_model:
                current_active_model.is_active = False

            if new_active_model:
                new_active_model.is_active = True
                new_active_model.activated_at = datetime.now()

            db.commit()

            logger.info(f"Successfully activated model ID: {new_active_id}")

        except Exception:
            db.rollback()
            logger.exception(f"Failed to switch active model to ID: {new_active_id}")
            raise        
        
        
        
def get_first_model() -> ModelRegistry | None:

    with db_connect() as db:

        logger.info("Fetching first model record")

        try:

            model_record = (
                db.query(ModelRegistry)
                .order_by(ModelRegistry.id.asc())
                .first()
            )

            if model_record is None:
                logger.warning("No model records found in database")
                return None

            logger.info(f"First model record found. ID: {model_record.id}")
            return model_record

        except Exception:
            logger.exception("Failed to fetch first model record")
            raise        
        
        
        
def activate_initial_model(
    model_id: int
) -> None:

    with db_connect() as db:

        logger.info(f"Activating initial model ID: {model_id}")

        try:

            model_record = (
                db.query(ModelRegistry)
                .filter(ModelRegistry.id == model_id)
                .first()
            )

            if model_record is None:

                logger.warning(f"No model found for ID: {model_id}")

                return

            model_record.is_active = True
            model_record.activated_at = datetime.now()

            db.commit()

            logger.info(f"Initial model activated successfully. ID: {model_id}")

        except Exception:

            db.rollback()

            logger.exception(f"Failed to activate initial model ID: {model_id}")

            raise        