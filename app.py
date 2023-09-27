from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List, Union, Any
import uvicorn, os, sys, datetime
import logging
from logging_lib import RouterLoggingMiddleware
from src.connectors.metastore import MongoDBConnector
from src.connectors.datastore import AzureBlobCreator, AzureContainerCreator, AzureStorageConnector, \
                             AzureFileShareConnector, AzureFileShareDirectoryCreator, AzureFileShareFileUploader


MEDIA_TYPE = "application/json"

mongodb_client_creator = MongoDBConnector() # creation of mongodb client
mongodb_client = mongodb_client_creator.create_connector(db_name='ris_data_collection')

file_share_client_creator = AzureFileShareConnector() # file share client
file_share_client = file_share_client_creator.connect('myshare1')

directory_creator = AzureFileShareDirectoryCreator(file_share_client) # azurecontainer creator and blob creator
file_uploader = AzureFileShareFileUploader(file_share_client)


def get_application() -> FastAPI: # Define application
    app = FastAPI(title="DataCollection-Server", debug=True) ## instantitaing fastapi 

    return app

app = get_application() # Initialize application

@app.get("/") ## fetching all labels from mongodb 
def home():
    """
    Takes us directly to the /docs route.
    """
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/labels") ## fetching all labels from mongodb 
def fetch_label():
    """
    Fetches the labels from the MetaData Store.
    """
    try:
        #global labels
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document.get('class_name') for document in results]
        response = {"Status": "Success", "Response": {'labels': documents}}
        return JSONResponse(content=response, status_code=200, media_type=MEDIA_TYPE)

    except Exception as e:
        raise e
        

@app.get("/label_count") ## fetching all labels from mongodb 
def fetch_label():
    """
    Fetches the labels from the MetaData Store.
    """
    try:
        #global labels
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document.get('class_name') for document in results]
        response = {"Status": "Success", "Response": {'number of labels': len(documents)}}
        return JSONResponse(content=response, status_code=200, media_type=MEDIA_TYPE)

    except Exception as e:
        raise e


@app.post("/add_label/{label_name}") # adding new labels
def add_label(label_name: str):
    """
    Adds a specified label to metadata store, and datastore.
    """
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

            container_response = directory_creator.create(directory_name=label_name)  # create a container named label_name

        response = {"Status": "Success"}
        return JSONResponse(content=response, status_code=200, media_type=MEDIA_TYPE)

    except Exception as err:
        return err 


@app.get("/single_upload/") # upload single image 
def single_upload():
    """
    Gives the single upload page.
    """
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type=MEDIA_TYPE)


@app.post("/single_upload/") # Image Single Upload Api
async def single_upload(label: str, file: UploadFile = None):
    """
    Uploads the image file to the datastore.
    """
    try:
        collections = mongodb_client['labels']
        results = collections.find()
        documents = [document for document in results]

        class_names = [document.get('class_name') for document in documents]
        is_label_present = label in class_names
        file_contents = file.file.read() 
        #file_contents = open('image.jpeg', 'wb')

        if file.content_type == "image/jpeg" and is_label_present:
            func_response = file_uploader.upload(
                directory_name=label,
                file_content=file_contents,
                dst_file_name=file.filename
            )
            response = {"filename": file.filename, "label": label, "container-Response": func_response}
            return JSONResponse(content=response, status_code=200, media_type=MEDIA_TYPE)

        elif not file.content_type == "image/jpeg" and not is_label_present:
            response =  {
                "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
                "LabelNotFound": f"Label named: {label} not found, Add new label using /add_label endpoint"
            }

            return JSONResponse(content=response, status_code=400, media_type=MEDIA_TYPE)
        
        elif not file.content_type == "image/jpeg":
            response =  {
                "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            }
            return JSONResponse(content=response, status_code=400, media_type=MEDIA_TYPE)

        else:
            response =  {
                "LabelNotFound": f"Label named: {label} not found, Add new label using /add_label endpoint"
            }
            return JSONResponse(content=response, status_code=400, media_type=MEDIA_TYPE)

    except Exception as err:
        response = {"ContentType": f"Content type should be Image/jpeg not {e}"}
        return JSONResponse(content=response, status_code=400, media_type=MEDIA_TYPE)


@app.get("/bulk_upload") # router for bulk upload page.(get method)
def bulk_upload():
    """
    Gives the bulk upload page.
    """
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type=MEDIA_TYPE)


@app.post("/bulk_upload/") # route for bulk upload page(post method)
def bulk_upload(label: str, files: List[UploadFile] = File(...)):
    """
    Uploads the multiple image file to the datastore.
    """
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

            return JSONResponse(content=info, status_code=200, media_type=MEDIA_TYPE)

        else:
            return {
                "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
                "LabelFound": label,
            }

    except Exception as err:
         return {"ContentType": f"Content type should be Image/jpeg not {e}"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)