from pymongo.mongo_client import MongoClient 
from abc import ABC, abstractmethod, ABCMeta
import os, sys 
from logger import log_config
import logging


LOGGER = logging.getLogger(__main__)


# singleton pattern.
class SingletonABCMeta(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        

# database abstract class.
class DataBaseConnector(ABC):
    __metaclass__ = SingletonABCMeta
    def __init__(self):
        pass 

    @abstractmethod
    def create_connector(self):
        """
        this is a abstract method, in the abstract class, which has a header, but 
        no body.
        """
        pass 

# mongodb connector.
class MongoDBConnector(DataBaseConnector):
    """
    this class, used to connect to the mongodb database with the specified cluster, 
    and to the mongofb  
    """
    def __init__(self):
        pass 

    def create_connector(self, db_name: str):
        try:
            username = os.environ['MONGO_USERNAME']
            password = os.environ['MONGO_PASSWORD']

            uri = f'mongodb+srv://{username}:{password}@cluster0.kyobhtc.mongodb.net/?retryWrites=true&w=majority'
            client = MongoClient(uri)
            client_db = client[db_name]

            return client_db

        except Exception as err:
            LOGGER.error(f'Creation of MongoDB Connector failed, Reason: {err}')
            raise 