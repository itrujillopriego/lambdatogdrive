import json
import urllib.parse
import boto3
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import uuid
from urllib.parse import unquote_plus

            

print('Loading function')

s3 = boto3.client('s3')
## original code from lambda

# scope is setup in GCP , sercive account file is created also within GCP and needs to be set with specific permissions 
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "x.json" #insert your json credentials name, to be read from the source directory or env  

bucket_name="mdpilot-staging"
# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)
folder_id='x' #insert folder_id for file to be uploaded, you can add parent->child folders

def google_upload_file(drive_service, file_name_with_path, file_name, folder_id, mime_type):  
    """
    Uploads a file to Google Drive to the designated folder in a shared drive.
    
    Args:
        service: Google Drive API service instance.
        file_name_with_path: s3 object name and location
        file_name: Name of file to be saved to Google, and also for its title in the file metadata.
        description: Description of the file to insert, for the file metadata.
        folder_id: Parent folder's ID for the Google Drive shared folder where the file will be uploaded.
        mime_type: MIME type of the file to insert.
    
    Returns: file info
    """
    media_body = MediaFileUpload(file_name_with_path, mimetype=mime_type)

    body = {
        'name': file_name,
        'title': file_name,
        #'description': description, #I think this is optional
        'mimeType': mime_type,
        'parents': [folder_id]
    }
    
    # note that supportsAllDrives=True is required or else the file upload will fail
    file = drive_service.files().create(
        supportsAllDrives=True,
        body=body,
        media_body=media_body).execute()





    print('{}, {}'.format(file_name, file['id']))
    
    #return file




def handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        s3.download_file(bucket, key, download_path)
        google_upload_file(drive_service,download_path,key,folder_id,response['ContentType']) # content type has the corret value
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    


    
            

