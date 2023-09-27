from pymongo.mongo_client import MongoClient 
from abc import ABC, abstractmethod, ABCMeta
import os, sys 
sys.path.append('../')
from ..logger import * 
import logging


LOGGER = logging.getLogger(__name__)


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
        """
        this constructor, is empty because of it is inside of the DataBaseConnector
        Abstract class.
        """
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
        """
        MongoDBConnector's Constructor.
        """
        self.mongo_client = MongoClient 

    def create_connector(self, db_name: str):
        try:
            username = os.environ['MONGO_USERNAME']
            password = os.environ['MONGO_PASSWORD']

            uri = f'mongodb+srv://{username}:{password}@cluster0.kyobhtc.mongodb.net/?retryWrites=true&w=majority'
            client = self.mongo_client(uri)
            client_db = client[db_name]
            LOGGER.info('Sucessfully connected to the DataStore(MongoDB)')
            return client_db

        except Exception as err:
            LOGGER.error(f'Creation of MongoDB Connector failed, Reason: {err}')
            raise 

