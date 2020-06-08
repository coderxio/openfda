import os
import requests
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from db.models import Base
from utils.log import startLogging

logger = startLogging('connect_db')

def connection():
    # Connect to DB
    p = Path.cwd()
    db = f"sqlite:///drugs.db"
    logger.debug(db)
    engine = create_engine(os.environ.get('DB_URI', db))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
