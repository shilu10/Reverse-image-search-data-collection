import os, sys 
sys.paths.append('..')
from abc import abstractmethod, ABC
from exceptions.metastore import CustomException
from connectors.metastore import MongoDBConnector


class MetaDataStore(ABC):
    def __init__(self, *args, **kwargs):
        pass 

    def register_labels(self):
        pass 

    def run(self):
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
        self.data_path = 'reverse_image_search_data/caltech-101/'
    
    def register_labels(self):
        """
        this method, will connect to the monogodb database, and create a new
        documents for each label.
        """
        try:
            print('[+]Started Inerting the labels into meta datastore')
            if not os.path.exists(self.data_path):
                raise CustomException('No file or directory, is found in the path, try to run datastore_setup.py first', '') 
            
            all_dirs = os.listdir(self.data_path)
            print(all_dirs)
            collections = self.__mongo_client['labels']
            prin(collection)
            results = collections.find()
            print(results)
            if len(documents) > 0:
                documents = [doc.get('class_id') for doc in results]
                if 0 in documents:
                    raise CustomException('Labels already present in the metadata store', '')

            else:
                for class_id, class_name in enumerate(all_dirs):
                    new_doc = {
                        'class_id': class_id,
                        'class_name': class_name
                    }

                    collections.insert_one(new_doc)

            print('[+]Completed inserting all labels into metadata store.')

        except Exception as err:
            print(err)
            return 

    def run(self):
        try:
            self.register_labels()
        
        except Exception as err:
            return err
            

if __name__ == '__main__':
    mongo_client_obj = MongoDBConnector()
    mongo_client = mongo_client_obj.create_connector('ris_data_collection')
    metastore = MongoDBMetaDataStore(mongo_client)
    metastore.run()