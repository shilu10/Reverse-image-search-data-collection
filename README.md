# Reverse-image-search-data-collection


### to get the storage account key

	az storage account keys list --resource-group  resource_group --account-name storage_acc_name

	storage key = QxedQzl2GHeH57C5rPtuECF8ROHSU4QUeVrdHOBUEJnf/D9yuX11cwjNSJg2+FJ+5lBIEc11QxvZ+ASt/IqVTQ==

	# outputs a key, make it as a environment variable, it will be used by python api to create a container in azure.

	environment variables we need,
	MONGO_USERNAME 
	MONGO_PASSWORD
	AZ_ACCOUNT_KEY


sas_token = generate_account_sas(
    account_name="tfstate686",
    account_key="QxedQzl2GHeH57C5rPtuECF8ROHSU4QUeVrdHOBUEJnf/D9yuX11cwjNSJg2+FJ+5lBIEc11QxvZ+ASt/IqVTQ==",
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)


### to get a connection string, used by the share_client
az storage account show-connection-string -g tfstate -n tfstate686

share = ShareClient.from_connection_string(conn_str=conn_str, share_name="myshare")


### to generate the sas token(used by azcopy as autenticatin token)
	 az storage file generate-sas --share-name myshare --account-name tfstate686 --permission rcdw --path reverse_image_search_data --expiry 2037-12-31T23:59:00Z


### to copy file from local to fileshare azure;
	# url:
		# file_share and directory in the fileshare 
			/myshare/reverse_image_search_data/
			
		https://tfstate686.file.core.windows.net/myshare/reverse_image_search_data/

	azcopy copy 'data.txt' 'https://tfstate686.file.core.windows.net/myshare/reverse_image_search_data/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2023-09-18T08:33:39Z&st=2023-09-18T00:33:39Z&spr=https,http&sig=fJ7w2frsgEd696k%2BKV50QEuSbqDQlMyEYBLQ2xx40cY%3D' --recursive
