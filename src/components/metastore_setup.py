import os, sys 
sys.path.append('..')
from abc import abstractmethod, ABC
from exceptions.metastore import CustomException, LabelPresentException
from connectors.metastore import MongoDBConnector
from logger import log_config
import logging


LOGGER = logging.getLogger(__name__)


class MetaDataStore(ABC):
    def __init__(self, *args, **kwargs):
        pass 

    def register_labels(self):
        """
        this is an abstractmethod from the abstract class named MetaDataStore.
        the implementation(body) of this method will be empty.
        """
        pass 

    def run(self):
        """
        this is an abstractmethod from the abstract class named MetaDataStore.
        the implementation(body) of this method will be empty.
        """
        pass 


class MongoDBMetaDataStore(MetaDataStore):
    """
    this class, used to create a metadata store for storing the labels, here
    mongodb is used as a metadata store.
    methods:
        register_labels(type: public)
    attrs:
        __mongo_client(type: MongoDBClient): mongo_client, for connecting to th db.
        data_path(dtype: str): path to which the initial data is stored.
    """
    def __init__(self, mongo_client):
        self.__mongo_client = mongo_client
        self.data_path = 'reverse_image_search_initial_data/caltech-101/'
    
    def register_labels(self):
        """
        this method, will connect to the monogodb database, and create a new
        documents for each label.
        """
        try:
            LOGGER.infor("Started Inerting the metadata(label details) into metadatastore")
            if not os.path.exists(self.data_path):
                raise CustomException('No file or directory, is found in the path, try to run datastore_setup.py first', '') 
            
            all_dirs = os.listdir(self.data_path)
            collections = self.__mongo_client['labels']
            results = collections.find()
            documents = [document for document in results]
            if len(documents) > 0:
                documents = [doc.get('class_id') for doc in results]
                if 0 in documents:
                    raise LabelPresentException('Labels already present in the metadata store', '')

            else:
                for class_id, class_name in enumerate(all_dirs):
                    try:
                        new_doc = {
                            'class_id': class_id,
                            'class_name': class_name
                        }

                        collections.insert_one(new_doc)

                    except Exception as err:
                        LOGGER.error(f"Error during inserting label record to metadata sore, Reason: {err}")
                        return 

                return {"Process": "Success"}

            LOGGER.infor("Completed inserting all labels into metadata store.")

        except CustomException as err:
            LOGGER.error(f"There is no file or directory named present in {data_path}, so try to run datastore_setup.py first")
            return 

        except Exception as err:
            LOGGER.error(f"There is error during registering label details into meta datastore. Error: {err}")
            return 

        except LabelPresentException as err:
            LOGGER.error("Label already present in the metadata store")
            return 

    def run(self):
        try:
            response = self.register_labels()
            if response:
                LOGGER.info("inserting label details in metadata store is successfull.")
        
        except Exception as err:
            LOGGER.error("inserting label details in metadata store is Failed.")
            

if __name__ == '__main__':
    mongo_client_obj = MongoDBConnector()
    mongo_client = mongo_client_obj.create_connector('ris_data_collection')
    metastore = MongoDBMetaDataStore(mongo_client)
    metastore.run()