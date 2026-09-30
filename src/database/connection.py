from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from contextlib import contextmanager
from src.utils.logs_handler import logger
from src.config.config import ENV

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/driftshield"

engine = create_engine(ENV.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


Base.metadata.create_all(bind=engine)


@contextmanager
def db_connect():
    db = SessionLocal()
    logger.debug("Database session created")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")
