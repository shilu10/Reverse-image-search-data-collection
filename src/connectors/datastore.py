from abc import ABC, abstractmethod
import os, sys
sys.path.append('..')
from typing import Dict
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from azure.storage.fileshare import ShareClient
from io import BufferedReader
from ..logger import *
import logging


LOGGER = logging.getLogger(__name__)

class DataStoreConnector(ABC): 
	def __init__(self):
		"""
        this constructor, is empty because of it is inside of the DataStoreConnector
        Abstract class.
        """
		pass 

	@abstractmethod
	def connect(self):
		"""
		this method implementation is empty, bcox this is abstract method, inside
		a DataStoreConnector Abstract Class
		"""
		pass 


class CreateDirectory(ABC):
	def __init__(self):
		"""
		this constructor, is empty because of it is inside of the CreateDirectory
    	Abstract class.
		"""
		pass 

	@abstractmethod
	def create(self):
		"""
		this method implementation is empty, bcox this is abstract method, inside
		a CreateDirectory Abstract Class
		"""
		pass 


class UploadData(ABC):
	def __init__(self):
		"""
		this constructor, is empty because of it is inside of the UploadData
    	Abstract class.
		"""
		pass 

	@abstractmethod
	def upload(self):
		"""
		this method implementation is empty, bcox this is abstract method, inside
		a UploadData Abstract Class
		"""
		pass 


class AzureStorageConnector(DataStoreConnector):
	"""
	this class, is used to create a block blob storage connector, which 
	allow us to create container and create blob.
	methods;
		connect(public): which creates stroage connector, to specified storage 
		account.
	attrs:
		acc_name(dtype: str): To which storage account, needed to be connected.
	"""
	#blob_
	def __init__(self, acc_name: str):
		self.acc_name = acc_name
		self.block_service_client = BlockBlobService

	def connect(self) -> BlockBlobService:
		try:
			block_blob_service = self.block_service_client(account_name=self.acc_name, account_key=os.environ['AZ_ACCOUNT_KEY'])

			return block_blob_service

		except Exception as err:
			LOGGER.error(f'Creation of Azure storage account connector failed. Reason: {err}')
			raise  


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

		 	return {'container_creation_response': True}

		except Exception as err:
			LOGGER.error(f'Creation of Blob Container Failed, Reason: {err}')
			return {'container_creation_response': False} 


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

			return {'blob_creation_response': True}

		except Exception as err:
			LOGGER.error(f'Uploading of file to blob storage failed., Reason: {err}')
			return {'blob_creation_response': False}


### creating nfs share for storing training_data.
class AzureFileShareConnector(DataStoreConnector):
	"""
	this class, is used to create a connector to the nfs(azure file share), 
	so, this connection string, can be used by other classes.
	methods;
		connect(public): which creates stroage connector, to specified storage 
		account.
	attrs:
		acc_name(dtype: str): To which storage account, needed to be connected.
	"""
	def __init__(self):
		"""
		AzureFileShareConnector's Constructor.
		"""
		self.share_client = ShareClient 

	def connect(self, share_name: str)->ShareClient:
		try:
			connection_string = os.environ['AZ_CONNECTION_STRING']
			share = self.share_client.from_connection_string(connection_string, share_name)
			LOGGER.info(f'Successfully created, the Azure File share creator')
			return share 

		except Exception as err:
			LOGGER.error(f'Creation of Azure File share creator failed. Reason: {err}')
			raise 


class AzureFileShareDirectoryCreator(CreateDirectory):
	"""
	this call, is used to create a directory in the azurefileshare(nfs),
	so, it can be used to create a directory
	methods:
		create(public): this methods, will creates the directory
	attrs:
		share_client(type; BlockBlobService): client created from 
													ShareClient.
	"""
	def __init__(self, share_client):
		self.__share_client = share_client

	def create(self, directory_name: str)->Dict:
		"""
		this method, will create the directory in the specific share in storage
		account, which is provided throught the share_client.
		Params:
			directory_name(dtype: str): name of the container needed to be
											created.
		Return(dtype: dict):
			ir returns the dictonary of the response from the azure,
		"""
		try:
			# create root direc(reverse_image_search_data)
			self.__share_client.create_directory(f"reverse_image_search_data/train/{directory_name}")
			LOGGER.info(f'Successfully created, the Azure File share Directory named: {directory_name}')
			return {'fileshare_directory_creation_response': True}

		except Exception as err:
			LOGGER.error(f'Creation of File Share Directory Failed, Reason: {err}')
			return {'fileshare_directory_creation_response': False}


class AzureFileShareFileUploader(UploadData):
	"""
	this class, is used to create a file in specific directory path in 
	the azure file share.
	methods:
		upload(public): this method, will upload the data to file.
	attrs;
		share_client(type; BlockBlobService): client created from 
													ShareClient.
	"""
	def __init__(self, share_client):
		self.__share_client = share_client

	def upload(self, directory_name: str, 
				file_content: BufferedReader, dst_file_name: str)->Dict:
		"""
		this method, will upload the file from local node to the 
		destinated container as a fileshare directory.
		params;
			directory_name(dtype: str): container to where, the blob will be
											created.
			file_path(dtype: str): local path, where the file is located
			dst_file_name(dtype: str): name for the blob, that will be created.
		"""
		try:
			parent_dir = f"reverse_image_search_data/train/{directory_name}"
			dir_client = self.__share_client.get_directory_client(parent_dir)

			dir_client.upload_file(data=file_content, file_name=dst_file_name)
			LOGGER.info(f'Successfully uploaded, the file named: {file_name} to Azure File share Directory named: {directory_name}')

			return {'fileshare_file_upload': True}

		except Exception as err:
			LOGGER.error(f'Uploading of file to fileshare directory failed., Reason: {err}')
			return {'fileshare_file_upload': False}
