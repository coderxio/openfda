import requests
import sys
import json
from connect_db import Drugs, Routes, ProductTypes, PharmClasses
from helpers import startLogging

logger = startLogging('load_ndcs')

def buildProductTypes(session, data):
    responses = set()
    try:
        for item in data['results']:
            try:
                responses.add(item['product_type'])
            except:
                pass
    except:
        logger.error("Failed to load responses table")
        return
    logger.debug(f"New data product_type(s): {str(responses)}\n")
    for item in responses:
        logger.info(f"New response added: {item}\n")
        row = ProductTypes(product_type = item)
        session.add(row)

def addData(session, data):
    try:
        try:
            product_id = data['product_id']
        except:
            logger.warning(f"A product ID does not exists for {data['generic_name']}")
            return
        try:
            generic_name = data['generic_name'].lower()[:300]
        except:
            generic_name = ""
        try:
            brand_name = data['brand_name'].lower()[:300]
        except:
            brand_name = ""
        try:
            classList = []
            for classItem in data['pharm_class']:
                classList.append(classItem)
        except:
            classList = []
        try:
            routesList = []
            for route in data['route']:
                routesList.append(route.lower())
        except:
            routesList = []
        try:
            form = data['dosage_form'].lower()[:100]
        except:
            form = ""
        try:
            productTypeId = session.query(ProductTypes.id).filter(ProductTypes.product_type == data['product_type'])
        except:
            productTypeId = None
    except:
        logger.error(f"JSON failure\n")
        return
    exists = session.query(Drugs).filter(Drugs.product_id == product_id).scalar()
    if not exists:
        logger.info(f"New data added: {generic_name}|{brand_name}|{form}|{product_id}\n")
        row = Drugs(product_id=product_id, generic_name=generic_name, brand_name=brand_name, dosage_form=form, product_type = productTypeId)            
        session.add(row)
        for route in routesList:
            logger.info(f"New data added: {generic_name}|{route}\n")
            route_row = Routes(route=route, dx_route=row)
            session.add(route_row)
        for pharmClass in classList:
            logger.info(f"New data added: {generic_name}|{pharmClass}\n")
            class_row = PharmClasses(pharm_class=pharmClass, dx_pharmClass=row)
            session.add(class_row)
    else:
        logger.warning(f"Data already exists: {product_id}|{generic_name}|{brand_name}\n")
    session.commit()
    return


def clear_tables(session):
    # Clear all current tables of information
    session.query(Routes).delete()
    session.query(PharmClasses).delete()
    session.query(Drugs).delete()
    session.query(ProductTypes).delete()


def main(session):
    f = open('data/drug-ndc-20200504.json')
    data = json.load(f)

    # Need a flag / config / etc. to drop tables on demand for rebuild.

    # Need improved process to minimze circling through JSON file twice.
    buildProductTypes(session, data)
    for line in data['results']:
        logger.debug(f"{line}")
        addData(session, line)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception('Unhandled Exception')