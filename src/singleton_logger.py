#-*-coding:utf-8-*-
import logging.config
import logging 
from logging import config
import os
from datetime import datetime


LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
            filename=LOG_FILE_PATH,
            format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()


@singleton
class Logger():
    def __init__(self):
        self.logr = logging.getLogger('root')