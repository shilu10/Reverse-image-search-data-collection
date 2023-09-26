import unittest, sys 
sys.path.append('..')
import pytest 
from unittest.mock import patch
from src.connectors import datastore, metastore
#import azure 

class TestAzureBlobStorage(unittest.TestCase):
	#@pytest.fixture(autouse=True)
	@patch('azure.storage.blob.BlockBlobService')
	def test_connect(self, mock_blob_service_client): 
		print(mock_blob_service_client)
		# name of storage acc 
		acc_name = ''
		datastore_connector = datastore.AzureStorageConnector(acc_name)
		print(datastore_connector.block_service_client)
		# Define a mock blob client that will return the expected file data
		mock_blob_client = mock_blob_service_client
		mock_blob_client.return_value = ""
		
		datastore_connector.block_service_client = mock_blob_client
		print(datastore_connector.block_service_client)
		return_val = datastore_connector.connect()

		assert return_val == ""

	#@pytest.fixture(autouse=True)
	@patch('azure.storage.blob.BlockBlobService')
	def test_create(self, mock_blob_service_client):
		# add a container creator return values
		mock_blob_service_client.create_container.return_value = True 
		mock_blob_service_client.set_container_acl.return_value = True 
		container_creator = datastore.AzureContainerCreator(mock_blob_service_client)

		container_name = ""
		is_public = True 
		container_creation_res = container_creator.create(container_name, is_public)

		assert container_creation_res == {'container_creation_response': True} 

	@patch('azure.storage.blob.BlockBlobService')
	def test_upload(self, mock_blob_service_client):

		mock_blob_service_client.create_blob_from_path.return_value = True 
		container_name = ''
		blob_name = ''
		file_path = ''
		blob_creator_obj = datastore.AzureBlobCreator(mock_blob_service_client)
		response = blob_creator_obj.upload(container_name, blob_name, file_path)

		assert response == {'blob_creation_response': True}


class TestAzureFileShare(unittest.TestCase):
	@patch('azure.storage.fileshare.ShareClient')
	def test_connect(self, mock_share_client):
		mock_share_client.from_connection_string.return_value = ''

		fileshare_client_obj = datastore.AzureFileShareConnector()
		fileshare_client_obj.share_client = mock_share_client

		response = fileshare_client_obj.connect('')
		assert '' == response

	@patch('azure.storage.fileshare.ShareClient')
	def test_create(self, mock_share_client):
		mock_share_client.create_directory.return_value = ''
		fileshare_dir_creator = datastore.AzureFileShareDirectoryCreator(mock_share_client)

		directory_name = ''
		res = fileshare_dir_creator.create(directory_name)

		assert res == {'fileshare_directory_creation_response': True}

	@patch('azure.storage.fileshare.ShareClient')
	def test_upload(self, mock_share_client):
		mock_share_client = mock_share_client.get_directory_client.return_value 
		mock_share_client.upload_file.return_value = ''
		fileshare_dir_creator = datastore.AzureFileShareDirectoryCreator(mock_share_client)

		directory_name = ''
		file_content = ''
		dst_file_name = ''
		res = fileshare_dir_creator.create(directory_name)

		assert res == {'fileshare_directory_creation_response': True}


class TestMongoDBConnection(unittest.TestCase):
	@patch('pymongo.mongo_client.MongoClient')
	def test_create_connection_success(self, mock_mongo_client):
		mock_mongo_client.return_value = {'db_name': 'db_res'}
		
		metastore_creator = metastore.MongoDBConnector()
		metastore_creator.mongo_client = mock_mongo_client

		res = metastore_creator.create_connector('db_name')

		assert res == 'db_name'

	@patch('pymongo.mongo_client.MongoClient')
	def test_create_connection_success(self, mock_mongo_client):
		mock_mongo_client.return_value = {'db_name': 'db_res'}
		
		metastore_creator = metastore.MongoDBConnector()
		metastore_creator.mongo_client = mock_mongo_client

		res = metastore_creator.create_connector('db_name')

		assert res != ''
