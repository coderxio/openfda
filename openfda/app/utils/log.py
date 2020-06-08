'''
list of functions used throughout the application
'''

# Function that returns the logger
import logging
import datetime
from pathlib import Path

def startLogging(logger_name):
    # where do you want to place your log files?
    LOG_DIR = Path(__file__).parent.absolute() / 'log' / datetime.datetime.now().strftime("%Y")
    # make the log directory if it does not exist
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%Y/%m/%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    # enable file logging
    log_filename = datetime.datetime.now().strftime("%y%m%d_") + logger_name + '.log'
    filehandler = logging.FileHandler(LOG_DIR / log_filename)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    # enable console logging
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)
    return logger
