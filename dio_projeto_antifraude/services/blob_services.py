from azure.storage.blob import BlobServiceClient

from dio_projeto_antifraude.Config import Config


class BlobStorageService:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            Config.AZURE_STORAGE_CONNECTION
        )
    
    def upload_blob(self, file_path: str, file_name: str) -> str:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=Config.CONTAINER_NAME, blob=file_name
            )
            blob_client.upload_blob(file_path, overwrite=True)
            return blob_client.url
        except Exception as e:
            print(f'Erro no upload para o blob storage {e}')
            return None