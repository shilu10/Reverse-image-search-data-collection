from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Union, Any
import uvicorn
from src.connectors.database import DataBaseConnector
from src.connectors.feature_store import AzureBlobCreator, AzureContainerCreator, AzureStorageConnector


# creation of mongodb client
mongodb_client_creator = MongoDBConnector()
mongodb_client = mongodb_client_creator.create_connector(db_name='training_data')

# storage account client
blob_storage_client_creator = AzureStorageConnector(acc_name='training_data')
blob_storage_client = blob_storage_client_creator.connect()

# azurecontainer creator and blob creator
container_creator = AzureContainerCreator(blob_storage_client)
blob_creator = AzureBlobCreator(blob_storage_client)

## instantitaing fastapi 
app = FastAPI(title="DataCollection-Server")


## fetching all labels from mongodb 
@app.get("/labels")
def fetch_label():
    try:
        result = mongodb_client['labels'].find()
        documents = [document.get('class_name') for document in result]

        response = {"Status": "Success", "Response": {'labels': documents}}
        return JSONResponse(content=response, status_code=200, media_type="application/json")

    except Exception as e:
        raise e

# adding new labels
@app.post("/add_label/{label_name}")
def add_label(label_name: str):

    try:
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document for document in results]

        class_names = [document.get('class_name') for document in documents]
        class_ids = [document.get('class_id') for document in documents]

        if not label_name in class_names: 

            next_id = 0 
            if len(class_ids) > 0:
                last_id = max(class_ids) 
                next_id = last_id + 1 

            new_label_data = {
                'class_name': label_name,
                'class_id': next_id
            }

            collections.insert_one(new_label_data)

        response = {"Status": "Success"}
        return JSONResponse(content=response, status_code=200, media_type="application/json")

    except Exception as err:
        return err 


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080)
