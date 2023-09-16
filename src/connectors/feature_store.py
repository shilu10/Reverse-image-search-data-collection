from abc import ABC, abstractmethod
import os, sys
from typing import Dict
from azure.storage.blob import BlockBlobService



class FeatureStoreConnector(ABC): 
	def __init__(self):
		pass 

	@abstractmethod
	def connect(self):
		pass 


class CreateDirectory(ABC):
	def __init__(self):
		pass 

	@abstractmethod
	def create(self):
		pass 


class UploadData(ABC):
	def __init__(self):
		pass 

	@abstractmethod
	def upload(self):
		pass 


class AzureStorageConnector(FeatureStoreConnector):
	def __init__(self, acc_name):
		self.acc_name = acc_name

	def connect(self):
		try:
			block_blob_service = BlockBlobService(account_name=self.acc_name, 
												  account_key=os.environ['AZ_ACCOUNT_KEY'])

			return block_blob_service

		except Exception as err:
			return err 


class AzureContainerCreator(CreateDirectory):
	def __init__(self, blob_client):
		self.__blob_client = blob_client

	def create(self, container_name, is_public):
		try: 
		 	creation_response = self.__blob_client.create_container(container_name)
		 	if is_public and creation_response:
		 		self.__blob_client.set_container_acl(container_name, 
		 											public_access=PublicAccess.Container)

		 	return {'container_creation_response': creation_response}

		except Exception as err:
			return err 


class AzureBlobCreator(UploadData):
	def __init__(self, blob_client):
		self.__blob_client = blob_client

	def upload(self, container, image_path):
		try:
			self.__blob_client.create_blob_from_path(
						container_name = container,
						blob_name = "data.jpeg",
						file_path = image_path,
					)

			return {'response': True}

		except Exception as err:
			return err 
