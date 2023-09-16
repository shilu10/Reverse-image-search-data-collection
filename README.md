# Reverse-image-search-data-collection


### to get the storage account key

	az storage account keys list --resource-group  resource_group --account-name storage_acc_name

	storage key = QxedQzl2GHeH57C5rPtuECF8ROHSU4QUeVrdHOBUEJnf/D9yuX11cwjNSJg2+FJ+5lBIEc11QxvZ+ASt/IqVTQ==

	# outputs a key, make it as a environment variable, it will be used by python api to create a container in azure.

	environment variables we need,
	MONGO_USERNAME 
	MONGO_PASSWORD
	AZ_ACCOUNT_KEY


