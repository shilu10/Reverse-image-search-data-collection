from abc import ABC, abstractmethod
import os, sys
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from azure.storage.fileshare import ShareClient
from io import BufferedReader


class DataStore(ABC):
    def __init__(self):
        pass 

    @abstractmethod
    def download_data(self):
        pass 

    @abstractmethod
    def extract_initial_data(self):
        pass 

    @abstractmethod
    def prepare_initial_data(self):
        pass 

    @abstractmethod
    def create_initial_directories(self):
        pass 

    @abstractmethod
    def upload_initial_files(self):
        pass 


class AzureFileShareDataStore(DataStore):
    def __init__(self):
        self.dataset_name = "imbikramsaha/caltech-101" 
        self.extraction_path = "reverse_image_search_initial_data"
        self.avoid = ["BACKGROUND_Google"]
        self.data_path = self.extraction_path + '/caltech-101/'

    def download_data(self):
        try: 
            print("[+] Started downloading the dataset")
            if not os.path.exists(self.extraction_path):
                os.mkdir(self.extraction_path)

            command = f"cd {self.extraction_path} && kaggle datasets download -d {self.dataset_name}"
            os.system(command) 
            print("[+] Completed downloading the dataset")

        except Exception as err:
            return err 

    def extract_initial_data(self):
        try:
            print("[+] started extracting the dataset") 
            os.system("unzip caltech-101.zip")
            print("[+] extraction of the dataset completed.")

        except Exception as err:
            return err 

    def prepare_initial_data(self):
         

    def create_initial_directories(self):
        pass 

    def upload_initial_files(self):
        pass 