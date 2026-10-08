from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db_models import Base
from contextlib import contextmanager
from src.utils.logs_handler import logger
from src.config.config import ENV


engine = create_engine(ENV.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

@contextmanager
def db_connect():
    db = SessionLocal()
    logger.info("Database connection established")
    try:
        yield db
    finally:
        db.close()
        logger.info("Database connection closed")


# For Dependency
def get_db():
    db = SessionLocal()
    logger.info("Database connection established")
    try:
        yield db
    finally:
        db.close()
        logger.info("Database connection closed")