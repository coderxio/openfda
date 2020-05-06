import time
import sys
from load_ndcs import main as load_ndcs
from connect_db import main as connect_db
from server import main as cherrypy_server
from helpers import startLogging

logger = startLogging('run')


def main():
    # Allow the DB to set up completely.
    time.sleep(15)
    try:
        # Grab drug classes
        logger.debug("Connecting to database\n")
        session = connect_db()
    except:
        logger.warning("Failed connecting to database\n")
        time.sleep(60)
        logger.error("Second attempt connecting to database\n")
        session = connect_db()

    # cherrypy_server()
    load_ndcs(session)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception('Unhandled Exception') 
