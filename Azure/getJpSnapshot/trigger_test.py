import unittest
import azure.functions as func
from getJpSnapshot import main


from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

class TestFunction(unittest.TestCase):
    def test_my_function(self):
        # Construct a mock Queue message.
        req = func.TimerRequest

        # Call the function.
        main(req)

        connect_str = os.environ["AzureWebJobsStorage"]
        # Check the output.
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = 'jp-snapshots'
        container_client = blob_service_client.get_container_client(container_name)
        print(container_client.list_blobs())
    