from abc import ABC, abstractmethod
import os, sys
sys.path.append('..')
sys.path.append('../../')
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from azure.storage.fileshare import ShareClient
from io import BufferedReader
import shutil
from logger import log_config
import logging


LOGGER = logging.getLogger(__name__)


# abstract class (blueprint)
class DataStore(ABC):
    def __init__(self):
        """
        this constructor, is empty because of it is inside of the DataStore
        Abstract class.
        """
        pass 

    @abstractmethod
    def _download_data(self):
        """
        this is a abstract method inside a abstract class named DataStore, it 
        won't contain a body(implementation logic.)
        """
        pass 

    @abstractmethod
    def _extract_initial_data(self):
        """
        this is a abstract method inside a abstract class named DataStore, it 
        won't contain a body(implementation logic.)
        """
        pass 

    @abstractmethod
    def _prepare_initial_data(self):
        """
        this is a abstract method inside a abstract class named DataStore, it 
        won't contain a body(implementation logic.)
        """
        pass 

    @abstractmethod
    def _sync_initial_data(self):
        """
        this is a abstract method inside a abstract class named DataStore, it 
        won't contain a body(implementation logic.)
        """
        pass 

    @abstractmethod
    def run(self):
        """
        this is a abstract method inside a abstract class named DataStore, it 
        won't contain a body(implementation logic.)
        """
        pass 


class AzureFileShareDataStore(DataStore):
    """
    this class, contains a logic, which allows us to copy the initial 
    training data to the data_store. By default caltech-101 dataset is used.
    methods:
        __download_data(private)
        __extract_initial_data(private)
        __prepare_initial_data(private)
        __sync_initial_data(private)

    attrs:
        dataset_name(dtype: str): name of the initial dataset from kaggle.
        extraction_path(dtype: str): where to extract the initial dataset.
        avoid(dtype: List): list of classes, needed to be avoided.
        data_path(dtype: str): path of the data.
    """
    def __init__(self):
        self.dataset_name = "imbikramsaha/caltech-101" 
        self.extraction_path = "reverse_image_search_initial_data"
        self.avoid = ["BACKGROUND_Google"]
        self.data_path = self.extraction_path + '/caltech-101/'

    def _download_data(self):
        """
        this method, will download the data from kaggle, and extract it into 
        the extraction path.
        """
        try: 
            LOGGER.info(f"Started downloading the dataset from kaggle data namd {self.dataset_name}")
            if not os.path.exists(self.extraction_path):
                os.mkdir(self.extraction_path)

            command = f"cd {self.extraction_path} && kaggle datasets download -d {self.dataset_name}"
            os.system(command) 
            LOGGER.info(f" Completed downloading the dataset from kaggle data namd {self.dataset_name}")

        except Exception as err:
            LOGGER.error(f'Downloading of initial dataset from kaggle failed. Reason: {err}')
            return {"Response": "Failed"}

    def _extract_initial_data(self):
        """
        this method, will extract the initial data, using gzip and tar.
        """
        try:
            LOGGER.info("Started extracting the dataset, downloaded from kaggle.")
            if not os.path.exists(f'{self.extraction_path}/caltech-101'):
                os.system(f"cd {self.extraction_path} && unzip -q caltech-101.zip")
            LOGGER.info("Extraction of the dataset completed.")

        except Exception as err:
            LOGGER.error(f'Extraction of initial dataset downloaded from kaggle failed. Reason: {err}')
            return

    def _prepare_initial_data(self):
        """
        this method, used to prepare the data for the data_store, like removing the 
        unwanted classes, etc.
        """
        try:
            LOGGER.info("Started preparing the dataset.(Data Preparation)")
            classes = os.listdir(self.data_path)
            for _class in classes:
                if _class in self.avoid:
                    dir_path = self.data_path + f'{_class}'
                    shutil.rmtree(dir_path)

            LOGGER.info("Completed the preparation of the dataset")
        
        except Exception as err:
            LOGGER.error(f'Downloading of initial dataset from kaggle failed. Reason: {err}')
            return 
        
    def _sync_initial_data(self):
        """
        this method, used to sync the data from local storage to the data_store
        (file_share azure).
        """
        try:
            LOGGER.info("Started data sync to datastore using azcopy.")
            command = f"azcopy copy '{self.data_path}/*' '{os.environ['AZCOPY_URL']}' --recursive"
            os.system(command)
            LOGGER.info("Completed the data sync to datastore using azcopy.")
            return {"Process": "Success"}

        except Exception as err:
            LOGGER.error(f"There was a error during data sync using azcopy, Reason: {err}")
            return 

    def run(self):
        try:
            LOGGER.info("Started initial data upload process to datatore in datastore_setup.py.")
            
            self._download_data()
            self._extract_initial_data()
            self._prepare_initial_data()
            response = self._sync_initial_data()
            if response:
                LOGGER.info("Completed initial data upload process to datatore in datastore_setup.py.")

            else:
                LOGGER.error("Failed the process of initial data upload process to datatore in datastore_setup.py.")

        except KeyboardInterrupt:
            LOGGER.error('There is a manual cancellation of the process')
            sys.exit()

        except Exception as err:
            LOGGER.error(f'Initial data upload process stopped, due to {err}')
            sys.exit()

if __name__ == '__main__':
    ds = AzureFileShareDataStore()
    ds.run()
