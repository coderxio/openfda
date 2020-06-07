import os
import requests
import sys
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .models import Base
from helpers.helpers import startLogging

logger = startLogging('connect_db')

def connection():
    # Connect to DB
    p = Path.cwd()
    db = f"sqlite:///{p / 'data'}/drugs.db"
    logger.debug(db)
    engine = create_engine(os.environ.get('DB_URI', db))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
