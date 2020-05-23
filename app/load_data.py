import time
import sys
from load_data.load_ndcs import main as load_ndcs
from load_data.connect_db import main as connect_db
from helpers.helpers import startLogging
import get_data

logger = startLogging('run')


def main():
    try:
        logger.debug("Connecting to database\n")
        session = connect_db()
    except:
        logger.warning("Failed connecting to database\n")
        time.sleep(60)
        logger.error("Second attempt connecting to database\n")
        session = connect_db()

    load_ndcs(session)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception('Unhandled Exception') 
