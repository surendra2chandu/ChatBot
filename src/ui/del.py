from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from fastapi import HTTPException

class AzureBlobHandler:
    def __init__(self, storage_account_url: str, container_name: str):
        self.logger = logger
        self.container_name = container_name

        try:
            self.logger.info("Authenticating to Azure Blob Storage using DefaultAzureCredential...")
            credential = DefaultAzureCredential()
            self.blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
            self.container_client = self.blob_service_client.get_container_client(container_name)
            self.logger.info("Authenticated to Blob Storage successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Blob Storage connection: {e}")
            raise HTTPException(status_code=500, detail="Blob storage authentication failed.")

    def upload_blob(self, blob_name: str, data: bytes):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data, overwrite=True)
            self.logger.info(f"Uploaded blob '{blob_name}' successfully.")
        except Exception as e:
            self.logger.error(f"Error uploading blob '{blob_name}': {e}")
            raise HTTPException(status_code=500, detail=f"Error uploading blob: {e}")

    def download_blob(self, blob_name: str) -> bytes:
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob().readall()
            self.logger.info(f"Downloaded blob '{blob_name}' successfully.")
            return blob_data
        except Exception as e:
            self.logger.error(f"Error downloading blob '{blob_name}': {e}")
            raise HTTPException(status_code=500, detail=f"Error downloading blob: {e}")
