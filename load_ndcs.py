import requests
import sys
import json
from connect_db import Drugs


def add_data(session, data):
    try:
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
            classes = '|'.join(classList).lower()[:100]
        except:
            classes = ""
        try:
            routesList = []
            for route in data['route']:
                routesList.append(f"{route}")
            routes = '|'.join(routesList).lower()[:100]
        except:
            routes = ""
        try:
            form = data['dosage_form'].lower()[:100]
        except:
            form = ""
    except:
        sys.stderr.write(f"JSON failure\n")
        return
    exists = session.query(Drugs).filter(Drugs.generic_name == generic_name)\
                                 .filter(Drugs.brand_name == brand_name)\
                                 .filter(Drugs.route == routes)\
                                 .filter(Drugs.dosage_form == form)\
                                 .filter(Drugs.pharm_class == classes).scalar()
    if not exists:
        sys.stdout.write(f"New data added: {generic_name}|{brand_name}|{routes}|{form}\n")
        row = Drugs(generic_name=generic_name, brand_name=brand_name, route=routes, dosage_form=form pharm_class=classes)
        session.add(row)
    else:
        sys.stdout.write(f"Data already exists: {generic_name}|{brand_name}\n")
    session.commit()
    return


def main(session):
    f = open('data/drug-ndc-20200504.json')
    data = json.load(f)
    for line in data['results']:
        add_data(session, line)


if __name__ == "__main__":
    main()