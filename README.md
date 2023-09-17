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
    account_key=" QxedQzl2GHeH57C5rPtuECF8ROHSU4QUeVrdHOBUEJnf/D9yuX11cwjNSJg2+FJ+5lBIEc11QxvZ+ASt/IqVTQ==",
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)


### to get a connection string, used by the share_client
az storage account show-connection-string -g tfstate -n tfstate686

share = ShareClient.from_connection_string(conn_str=conn_str, share_name="myshare")
