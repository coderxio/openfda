import requests
import sys
import configparser
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Config settings under [database] section in settings.ini
def load_config():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['database']['use_docker']


# Table schema
Base = declarative_base()
class Drugs(Base):
    __tablename__ = "drug_info"

    id = Column(Integer, primary_key=True)
    generic_name = Column(String(300))
    brand_name = Column(String(300))
    pharm_class = Column(String(100))
    dosage_form = Column(String(100))
    route = Column(String(100))

    def __repr__(self):
        return "<Drugs(generic_name='%s', pharm_class='%s')>" % (
                    self.generic_name, self.pharm_class)

def main():
    # Connect to DB
    sys.stderr.write("Connecting to the DB")
    settings = load_config()
    if settings == 'yes':
        engine = create_engine('mysql+pymysql://admin:admin@db:3306/drugs')
    else:
        engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == "__main__":
    main()