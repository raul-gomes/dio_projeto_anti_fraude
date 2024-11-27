import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    AZURE_DOC_INT_ENDPOINT: str = os.getenv("AZURE_DOC_INT_ENDPOINT")
    AZURE_DOC_INT_KEY: str = os.getenv("AZURE_DOC_INT_KEY")
    AZURE_STORAGE_CONNECTION: str = os.getenv("AZURE_STORAGE_CONNECTION")
    CONTAINER_NAME: str = os.getenv("CONTAINER_NAME")
