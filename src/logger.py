#-*-coding:utf-8-*-
import logging.config
import logging 
from logging import config
import os, sys 
from datetime import datetime


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

