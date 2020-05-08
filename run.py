import sys
from load_ndcs import main as load_ndcs
from connect_db import main as connect_db
from server import main as cherrypy_server
from helpers import startLogging

logger = startLogging('run')


def main():
    # Allow the DB to set up completely.
    session = connect_db()
    
    # cherrypy_server()
    load_ndcs(session)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception('Unhandled Exception') 
