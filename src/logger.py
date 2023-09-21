#-*-coding:utf-8-*-
import logging.config
import logging 
from logging import config
import os
from datetime import datetime



LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

log_config = logging.basicConfig(
                filename=LOG_FILE_PATH,
                format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                level=logging.INFO,
            )



