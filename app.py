from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Union, Any
import uvicorn
from src.connectors.metastore import MongoDBConnector
from src.connectors.datastore import AzureBlobCreator, AzureContainerCreator, AzureStorageConnector, \
                             AzureFileShareConnector, AzureFileShareDirectoryCreator, AzureFileShareFileUploader



# creation of mongodb client
mongodb_client_creator = MongoDBConnector()
mongodb_client = mongodb_client_creator.create_connector(db_name='ris_data_collection')

# storage account client
#blob_storage_client_creator = AzureStorageConnector(acc_name='tfstate686')
#blob_storage_client = blob_storage_client_creator.connect()

# file share client
file_share_client_creator = AzureFileShareConnector()
file_share_client = file_share_client_creator.connect('myshare')

# azurecontainer creator and blob creator
directory_creator = AzureFileShareDirectoryCreator(file_share_client)
file_uploader = AzureFileShareFileUploader(file_share_client)

## instantitaing fastapi 
app = FastAPI(title="DataCollection-Server")

## fetching all labels from mongodb 
@app.get("/labels")
def fetch_label():
    try:
        global labels
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document.get('class_name') for document in results]
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

            # create a container named label_name
            container_response = directory_creator.create(directory_name=label_name)
            print(container_response)

        response = {"Status": "Success"}
        return JSONResponse(content=response, status_code=200, media_type="application/json")

    except Exception as err:
        return err 


# upload single image 
@app.get("/single_upload/")
def single_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Image Single Upload Api
@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    try:
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document for document in results]

        class_names = [document.get('class_name') for document in documents]
        is_label_present = label in class_names
        file_contents = file.file.read() 
        #file_contents = open('image.jpeg', 'wb')

        if file.content_type == "image/jpeg" and is_label_present:
            response = file_uploader.upload(
                directory_name=label,
                file_content=file_contents,
                dst_file_name=file.filename
            )
            return {"filename": file.filename, "label": label, "container-Response": response}
        
        else:
            return {
                "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
                "LabelFound": label,
            }

    except Exception as err:
         return {"ContentType": f"Content type should be Image/jpeg not {e}"}


@app.get("/bulk_upload")
def bulk_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


@app.post("/bulk_upload/")
def bulk_upload(label: str, files: List[UploadFile] = File(...)):
    skipped = []
    uploaded = []
    try:
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document for document in results]

        class_names = [document.get('class_name') for document in documents]
        is_label_present = label in class_names

        if label:
            for file in files:
                file_contents = file.file.read() 
                if file.content_type == "image/jpeg":
                    response = file_uploader.upload(
                        directory_name=label,
                        file_content=file_contents,
                        dst_file_name=file.filename
                    )

                    uploaded.append(file.filename)

                else:
                    skipped.append(file.filename)

            info = {"Response": "Success", 
                    "Uploaded_files": uploaded,
                    "Skipped_files": skipped
                }

            return JSONResponse(content=info, status_code=200, media_type="application/json")

        else:
            return {
                "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
                "LabelFound": label,
            }

    except Exception as err:
         return {"ContentType": f"Content type should be Image/jpeg not {e}"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)