from abc import ABC, abstractmethod
import os, sys
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from azure.storage.fileshare import ShareClient
from io import BufferedReader
import shutil


# abstract class (blueprint)
class DataStore(ABC):
    def __init__(self):
        pass 

    @abstractmethod
    def _download_data(self):
        pass 

    @abstractmethod
    def _extract_initial_data(self):
        pass 

    @abstractmethod
    def _prepare_initial_data(self):
        pass 

    @abstractmethod
    def _sync_initial_data(self):
        pass 

    @abstractmethod
    def run(self):
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
            print("[+] Started downloading the dataset")
            if not os.path.exists(self.extraction_path):
                os.mkdir(self.extraction_path)

            command = f"cd {self.extraction_path} && kaggle datasets download -d {self.dataset_name}"
            os.system(command) 
            print("[+] Completed downloading the dataset")

        except Exception as err:
            print(err)
            return 

    def _extract_initial_data(self):
        """
        this method, will extract the initial data, using gzip and tar.
        """
        try:
            print("[+] started extracting the dataset") 
            if not os.path.exists(f'{self.extraction_path}/caltech-101'):
                os.system(f"cd {self.extraction_path} && unzip -q caltech-101.zip")
            print("[+] extraction of the dataset completed.")

        except Exception as err:
            print(err) 
            return

    def _prepare_initial_data(self):
        """
        this method, used to prepare the data for the data_store, like removing the 
        unwanted classes, etc.
        """
        try:
            print('[+]Started preparing the dataset.')
            classes = os.listdir(self.data_path)
            for _class in classes:
                if _class in self.avoid:
                    dir_path = self.data_path + f'{_class}'
                    shutil.rmtree(dir_path)

            print('[+]Completed the preparation of the dataset')
        
        except Exception as err:
            print(err)
            return 
        
    def _sync_initial_data(self):
        """
        this method, used to sync the data from local storage to the data_store
        (file_share azure).
        """
        try:
            print('[+] Started the data sync') 
            command = f"azcopy copy '{self.data_path}/*' '{os.environ['AZCOPY_URL']}' --recursive"
            print(command)
            os.system(command)
            print('[+] Completed the data sync to datastore')
        
        except Exception as err:
            print(err)
            return 

    def run(self):
        try:
            self._download_data()
            self._extract_initial_data()
            self._prepare_initial_data()
            self._sync_initial_data()
        
        except Exception as err:
            print(err)
            return 


if __name__ == '__main__':
    ds = AzureFileShareDataStore()
    ds.run()
