from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from dio_projeto_antifraude.Config import Config

class CreditCardValidator:
    
    def __init__(self):
        self.credential = AzureKeyCredential(Config.AZURE_DOC_INT_KEY)
        self.document_client = DocumentIntelligenceClient(
            Config.AZURE_DOC_INT_ENDPOINT, self.credential
        )
        
    def detect_credit_card_info_from_url(self, card_url: str) -> dict:
        try:
            card_info = self.document_client.begin_analyze_document(
                "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url)
            ).result()
            for document in card_info.documents:
                fields = document.fields
                return {
                    "card_name": fields.get("CardHolderName", {}).get("content", ""),
                    "card_number": fields.get("CardNumber", {}).get("content", "").replace(" ", ""),
                    "expiry_date": fields.get("ExpirationDate", {}).get("content", ""),
                    "bank_name": fields.get("IssuingBank", {}).get("content", ""),  
                }
            return None
        except Exception as e:
            print(f"Erro na detecção de cartão: {e}")
            return None
        