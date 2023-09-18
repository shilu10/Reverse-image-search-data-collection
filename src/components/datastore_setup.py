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
    def __download_data(self):
        pass 

    @abstractmethod
    def __extract_initial_data(self):
        pass 

    @abstractmethod
    def __prepare_initial_data(self):
        pass 

    @abstractmethod
    def __sync_initial_data(self):
        pass 

    def run(self):
        try:
            self.__download_data()
            self.__extract_initial_data()
            self.__prepare_initial_data()
            self.__sync_initial_data()
        
        except Exception as err:
            return err 


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

    def __download_data(self):
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
            return err 

    def __extract_initial_data(self):
        """
        this method, will extract the initial data, using gzip and tar.
        """
        try:
            print("[+] started extracting the dataset") 
            os.system("unzip caltech-101.zip")
            print("[+] extraction of the dataset completed.")

        except Exception as err:
            return err 

    def __prepare_initial_data(self):
        """
        this method, used to prepare the data for the data_store, like removing the 
        unwanted classes, etc.
        """
        try:
            classes = os.listdir(self.data_path)
            for _class in classes:
                if _class in self.avoid:
                    dir_path = self.data_path + '/_class'
                    shutil.rmtree(dir_path)
        
        except Exception as err:
            return err 
        
    def __sync_initial_data(self):
        """
        this method, used to sync the data from local storage to the data_store
        (file_share azure).
        """
        try:
            print('[+] Started the data sync') 
            os.system(F"azcopy copy 'caltech-101' {os.environ['AZCOPY_URL']} --recursive")
            print('[+] Completed the data sync to datastore')
        
        except Exception as err:
            return err 
