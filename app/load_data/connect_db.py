import os
import requests
import sys
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from load_data.models import Base
from helpers.helpers import startLogging

logger = startLogging('connect_db')

def main():
    # Connect to DB
    p = Path.cwd()
    db = f"sqlite:///{p.parent / 'data'}/drugs.db"
    logger.debug(db)
    engine = create_engine(os.environ.get('DB_URI', db))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

if __name__ == "__main__":
    main()
