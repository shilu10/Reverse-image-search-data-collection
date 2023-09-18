from pymongo.mongo_client import MongoClient 
from abc import ABC, abstractmethod, ABCMeta
import os, sys 


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
        pass 

# mongodb connector.
class MongoDBConnector(DataBaseConnector):
    def __init__(self):
        pass 

    def create_connector(self, db_name: str):
        username = os.environ['MONGO_USERNAME']
        password = os.environ['MONGO_PASSWORD']

        uri = f'mongodb+srv://{username}:{password}@cluster0.kyobhtc.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(uri)
        client_db = client[db_name]

        return client_db