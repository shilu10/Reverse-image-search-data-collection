# Reverse-image-search-data-collection


### to get the storage account key

	az storage account keys list --resource-group  resource_group --account-name storage_acc_name

	# outputs a key, make it as a environment variable, it will be used by python api to create a container in azure.