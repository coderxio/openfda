import requests
import time
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from helpers import startLogging


logger = startLogging('connect_db')

# Table schema
Base = declarative_base()

# Main table
class Drugs(Base):
    __tablename__ = "drug"

    id = Column(Integer, primary_key=True)
    product_id = Column(String(100))
    
    generic_name = Column(String(300))
    brand_name = Column(String(300))
    pharm_class = Column(String(100))
    dosage_form = Column(String(100))
    product_type = Column(Integer, ForeignKey('productType.id'))
    routes = relationship("Routes", backref='dx_route')
    pharm_classes = relationship("PharmClasses", backref="dx_pharmClass")

    def __repr__(self):
        return "<Drugs(generic_name='%s', brand_name='%s', pharm_class='%s')>" % (
                    self.generic_name, self.brand_name, self.pharm_class)


# Routes table
class Routes(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True)
    route = Column(String(100))
    drug_id = Column(Integer, ForeignKey('drug.id'))

    def __repr__(self):
        return "<Routes(route='%s')>" % (self.route)
    

# Pharmacology Class table
class PharmClasses(Base):
    __tablename__ = "pharmClass"

    id = Column(Integer, primary_key=True)
    pharm_class = Column(String(100))
    drug_id = Column(Integer, ForeignKey('drug.id'))

    def __repr__(self):
        return "<PharmClasses(pharm_class='%s')>" % (self.pharm_class)

# Product Type table
class ProductTypes(Base):
    __tablename__ = "productType"

    id = Column(Integer, primary_key=True)
    product_type = Column(String(30))

    def __repr__(self):
        return "<ProductTypes(product_type='%s')>" % (self.product_type)


def main():
    # Connect to DB
    db = 'mysql+pymysql://admin:admin@db:3306/drugs'

    # Allow for infinite tries to DB
    try:
        logger.debug(f"Attempting to connect to DB: {db}")
        engine = create_engine(db)
        Base.metadata.create_all(engine)
    except:
        logger.error(f"Failed to connect to the DB: {db}")
        not_connected = True
        while not_connected:
            try:
                sys.stderr.write("Attempting to connect to DB again")
                engine = create_engine(db)
                Base.metadata.create_all(engine)
                not_connected = False
            except:
                time.sleep(10)
                pass

    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear all current tables of information
    session.query(Routes).delete()
    session.query(PharmClasses).delete()
    session.query(Drugs).delete()
    session.query(ProductTypes).delete()

    return session

if __name__ == "__main__":
    main()