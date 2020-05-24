import time
import sys
from serve_data.server import main as cherrypy_server
from helpers.helpers import startLogging

logger = startLogging('run')


def main():
    cherrypy_server()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception('Unhandled Exception') 
