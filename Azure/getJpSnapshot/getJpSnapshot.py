import datetime
import logging
import tempfile
import requests

import azure.functions as func
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    try:
        print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
        # Retrieve the connection string for use with the application. The storage
        # connection string is stored in an environment variable on the machine
        # created after the application is launched in a console or with Visual Studio,
        # the shell or application needs to be closed and reloaded to take the
        # environment variable into account.
        connect_str = os.environ["AzureWebJobsStorage"]

        container_name = 'jp-snapshots'

        local_path = tempfile.gettempdir()
        todayFileName = 'AllPeoplesByCountry_' + str(datetime.datetime.today().date()) + '.csv'
        upload_file_path = os.path.join(local_path, todayFileName)
        
        #Data set for all people groups
        url = "https://joshuaproject.net/resources/datasets/1"
        response = requests.get(url)

        with open(upload_file_path,'wb') as f:
            f.write(response.content)

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=todayFileName)

        logging.info("\nUploading to Azure Storage as blob:\n\t" + todayFileName)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

    except Exception as ex:
        print('Exception:')
        print(ex)
        logging.info(ex)


