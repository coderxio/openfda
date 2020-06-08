from api.server import start_server
from utils.log import startLogging

logger = startLogging('run')

if __name__ == '__main__':
    try:
        start_server()
    except Exception as e:
        logger.exception('Unhandled Exception')
