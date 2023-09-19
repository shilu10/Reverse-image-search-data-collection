from abc import ABC, abstractmethod
import os, sys
sys.path.append('..')
from connectors.datastore import *
from exceptions.metastore import *
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from azure.storage.fileshare import ShareClient
from io import BufferedReader
import shutil
import glob 
from tqdm import tqdm


class BulkUpload: 
    def __init__(self):
        fileshare_conn_creator = AzureFileShareConnector()
        fileshare_connector = fileshare_conn_creator.connect('myshare')

        ## directory creator and fileuploader
        self.fileshare_directory_creator = AzureFileShareDirectoryCreator(fileshare_connector)
        self.fileshare_file_uploader = AzureFileShareFileUploader(fileshare_connector)

        self.extraction_path = "reverse_image_search_initial_data"
        self.dataset_name = "imbikramsaha/caltech-101" 
        self.avoid = ["BACKGROUND_Google"]
        self.data_path = self.extraction_path + '/caltech-101/'
        self.fileshare_connector = fileshare_connector

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

            else:
                print(f"[+]{self.data_path} directory already exists, it is possible that data exists in datastore.")
                client_res = input("Do you want to continue the process: yes or no: ")
                assert client_res in ['yes', 'no'], "Invalid Response, response should be either 'yes' or 'no'"

                if client_res == 'no':
                    sys.exit()

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

    def _bulk_upload_helper(self):
        """
        this method, used to upload the data to the datastore, using the 
        datastore connector.
        """
        print('[+]Started uploading the data to datastore.')
        all_dirs = os.listdir(self.data_path)
        
        for indx, dir in tqdm(enumerate(all_dirs), total=len(all_dirs)):
            try:
                dir_path = os.path.join(self.data_path, dir)
                self.fileshare_directory_creator.create(dir)

                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    try:
                        file_contents = open(file_path, 'rb')
                        self.fileshare_file_uploader.upload(
                            directory_name=dir,
                            file_content=file_contents,
                            dst_file_name=file
                        )

                    except Exception as err:
                        print(f'error: {err}, so file named {file} is skipped')
            
            except Exception as err:
                print(f'error: {err}, so directory named {dir} is skipped')

        print('[+]Completed the uploading of data to datastore')


    def bulk_upload(self):
       self._bulk_upload_helper()

    def run(self):
        print('[+]Started bulk upload process.')
        self._download_data()
        self._extract_initial_data()
        self._prepare_initial_data()
        self.bulk_upload()
        print('[+]Completed bulk upload process.')


if __name__ == '__main__':
    ds_bulk_upload = BulkUpload()
    ds_bulk_upload.run()



