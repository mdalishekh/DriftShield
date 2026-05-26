from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from contextlib import contextmanager
from src.utils.logs_handler import logger

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/driftshield"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Tables create karo
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