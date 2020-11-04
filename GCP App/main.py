import base64
import io
import requests
import datetime

from google.cloud import storage

import cloudstorage as gcs

def upload_jp_file(event, context):
     print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))
     
     """Uploads a file to the bucket."""
     bucket_name = "jp-snapshots"
     destination_blob_name = 'AllPeoplesByCountry_' + str(datetime.datetime.today().date()) + '.csv'
     url = "https://joshuaproject.net/resources/datasets/1"
     
     storage_client = storage.Client()
     bucket = storage_client.bucket(bucket_name)
     blob = bucket.blob(destination_blob_name)
     
     try:
         response = requests.get(url)
         write_retry_params = gcs.RetryParams(backoff_factor=1.1)
         gcs_file = gcs.open(destination_blob_name,
                      'w',
                      content_type='text/csv',
                      options={'x-goog-meta-foo': 'foo',
                               'x-goog-meta-bar': 'bar'},
                      retry_params=write_retry_params)
         gcs_file.write('abcde\n')
         gcs_file.write('f'*1024*4 + '\n')
         gcs_file.close()
         print("File {} uploaded to {}.".format(destination_blob_name,bucket_name)
          )
     except Exception as e:
          print(e)