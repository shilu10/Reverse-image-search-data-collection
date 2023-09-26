#-*-coding:utf-8-*-
import logging.config
import logging 
from logging import config
import os, sys 
from datetime import datetime


#if not os.path.exists('logs'):
 #   os.mkdir('logs')

#LOG_FILE_DIR = os.path.join(os.environ['HOME'], "Reverse-image-search-data-collection", "logs")
#LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"
#LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

#logging.basicConfig(
 #               filename=LOG_FILE_PATH,
  #              format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
   #             level=logging.INFO,
    #        )


# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno) %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ],
        "propagate": True
    }
}

logging.config.dictConfig(logging_config)

