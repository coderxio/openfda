import os
import requests
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from load_data.models import Base


def main():
    # Connect to DB
    sys.stderr.write("Connecting to the DB")
    engine = create_engine(os.environ.get('DB_URI', '../../sqlite:///drugs.db'))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

if __name__ == "__main__":
    main()
