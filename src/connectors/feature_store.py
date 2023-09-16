from abc import ABC, abstractmethod
import os, sys
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings


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
	"""
		this class, is used to create a block blob storage connector, which 
		allow us to create container and create blob.
		methods;
			connect(public): which creates stroage connector, to specified storage 
			account.
		attrs:
			acc_name(dtype: str): To which storage account, needed to be connected.
	"""
	def __init__(self, acc_name: str):
		self.acc_name = acc_name

	def connect(self) -> BlockBlobService:
		try:
			block_blob_service = BlockBlobService(account_name=self.acc_name, 
												  account_key=os.environ['AZ_ACCOUNT_KEY'])

			return block_blob_service

		except Exception as err:
			return err 


class AzureContainerCreator(CreateDirectory):
	"""
		This class, allow us to create a azure container, in the s
		pecified storage account,
		methods;
			create(public): which will create the containers.
		attrs:
			blob_client(type: BlockBlobService): client created from azurestorageconnector.
	"""
	def __init__(self, blob_client: BlockBlobService):
		self.__blob_client = blob_client

	def create(self, container_name: str, is_public: bool) -> Dict:
		"""
			this method, will create the container in the specific storage
			account, which is provided throught the blob_client.
			Params:
				container_name(dtype: str): name of the container needed to be
											created.
				is_pubic(dtype: bool): whether the container, should be publicly 
										accessble or not.
			Return(dtype: dict):
				ir returns the dictonary of the response from the azure,
		"""
		try: 
		 	creation_response = self.__blob_client.create_container(container_name)
		 	if is_public and creation_response:
		 		self.__blob_client.set_container_acl(container_name, 
		 											public_access=PublicAccess.Container)

		 	return {'container_creation_response': creation_response}

		except Exception as err:
			return err 


class AzureBlobCreator(UploadData):
	"""
		this class, will allow us to create the blob in the specified 
		container, of specific storage account.
		methods:
			upload(public): this method, will upload the data to blob.
		attrs;
			__blob_client(type; BlockBlobService): client created from 
													azurestorageconnector.
	"""
	def __init__(self, blob_client: BlockBlobService):
		self.__blob_client = blob_client

	def upload(self, container_name: str, file_path: str, blob_name: str) -> Dict:
		"""
			this method, will upload the file from local node to the 
			destinated container as a blob.
			params;
				container_name(dtype: str): container to where, the blob will be
											created.
				file_path(dtype: str): local path, where the file is located
				blob_name(dtype: str): name for the blob, that will be created.
		"""
		try:
			self.__blob_client.create_blob_from_path(
						container_name = container_name,
						blob_name = blob_name,
						file_path = file_path,
					)

			return {'response': True}

		except Exception as err:
			return err 
