import requests
import sys
import json
import time
from pathlib import Path
from db.models import Drugs, Routes, ProductTypes, PharmClasses
from db.connect import connection
from utils.log import startLogging

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
        exists = session.query(ProductTypes).filter(ProductTypes.product_type == item).scalar()
        if not exists:
            logger.debug(f"New response added: {item}\n")
            row = ProductTypes(product_type = item)
            session.add(row)

def buildRouteTypes(session, data):
    routes = set()
    try:
        for item in data['results']:
            try:
                for route in item['route']:
                    routes.add(route)
            except:
                pass
    except:
        logger.error("Failed to load routes table")
        return
    logger.debug(f"New data route(s): {str(routes)}\n")
    for item in routes:
        logger.debug(item)
        exists = session.query(Routes).filter(Routes.route == item).scalar()
        if not exists:
            logger.debug(f"New response added: {item}\n")
            row = Routes(route = item)
            session.add(row)


def buildDrugs(session, drugs_data):
    objects = []
    product_ids = []
    for data in drugs_data['results']:
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
                    route_id = session.query(Routes.id).filter(Routes.route == route)
                    routesList.append(route_id)
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
        # exists = session.query(Drugs).filter(Drugs.product_id == product_id).scalar()
        if product_id not in product_ids:
            product_ids.append(product_id)
            logger.debug(f"New data added: {generic_name}|{brand_name}|{form}|{product_id}\n")
            if len(routesList) == 3:
                route1 = routesList[0]
                route2 = routesList[1]
                route3 = routesList[2]
            elif len(routesList) == 2:
                route1 = routesList[0]
                route2 = routesList[1]
                route3 = None
            elif len(routesList) == 1:
                route1 = routesList[0]
                route2 = None
                route3 = None
            else:
                route1 = None
                route2 = None
                route3 = None
            row = Drugs(product_id=product_id, generic_name=generic_name, brand_name=brand_name, dosage_form=form, route1=route1, route2=route2, route3=route3, product_type=productTypeId)            
            objects.append(row)
            # for route in routesList:
            #     logger.info(f"New data added: {generic_name}|{route}\n")
            #     route_row = Routes(route=route, dx_route=row)
            #     objects.append(route_row)
            for pharmClass in classList:
                logger.debug(f"New data added: {generic_name}|{pharmClass}\n")
                class_row = PharmClasses(pharm_class=pharmClass, dx_pharmClass=row)
                objects.append(class_row)
        else:
            logger.warning(f"Data already exists: {product_id}|{generic_name}|{brand_name}\n")
    start = time.process_time()
    session.add_all(objects)
    session.commit()
    logger.info(f"Commit drugs db: {str(time.process_time() - start)}")
    return


def clear_tables(session):
    # Clear all current tables of information
    session.query(Routes).delete()
    session.query(PharmClasses).delete()
    session.query(Drugs).delete()
    session.query(ProductTypes).delete()


def main(session):
    p = Path.cwd()
    f = open(p / 'data' / 'drug-ndc.json')
    data = json.load(f)

    # Need a flag / config / etc. to drop tables on demand for rebuild.

    # Need improved process to minimze circling through JSON file twice.
    start = time.process_time()
    buildProductTypes(session, data)
    logger.info(f"Add product types: {str(time.process_time() - start)}")
    start = time.process_time()
    buildRouteTypes(session, data)
    logger.info(f"Add routes: {str(time.process_time() - start)}")
    start= time.process_time()
    buildDrugs(session, data)
    logger.info(f"Add drugs information: {str(time.process_time() - start)}")
    f.close()


if __name__ == "__main__":
    try:
        main(connection())
    except Exception as e:
        logger.exception('Unhandled Exception')
