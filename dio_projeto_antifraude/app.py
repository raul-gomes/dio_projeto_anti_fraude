import datetime
import streamlit as st

from services.blob_services import BlobStorageService
from services.credit_card_services import CreditCardValidator

# Inicialização de serviços globais
CREDIT_CARD_VALIDATOR = CreditCardValidator()
BLOB_STORAGE_SERVICE = BlobStorageService()

def process_card_analysis(uploaded_file):
    """
    Processa a imagem de cartão de crédito carregada.

    Args:
        uploaded_file (UploadedFile): Arquivo de imagem carregado

    Returns:
        tuple: Informações do cartão e resultado da validação, ou None
    """
    try:
        st.image(uploaded_file, caption="Imagem do Cartão", use_column_width=True)

        with st.spinner("Processando..."):
            file_name = uploaded_file.name
            file = uploaded_file.getvalue()
            blob_url = BLOB_STORAGE_SERVICE.upload_blob(file, file_name)

            if not blob_url:
                st.error("Erro ao carregar imagem para o Blob Storage.")
                return None

            card_info = CREDIT_CARD_VALIDATOR.detect_credit_card_info_from_url(blob_url)
            if not card_info:
                st.error("Não foi possível analisar o cartão.")
                return None

            validation_result = CREDIT_CARD_VALIDATOR.validate_card_info(card_info)
            return card_info, validation_result

    except Exception as e:
        st.error(f"Erro durante análise do cartão: {e}")
        return None

def card_analysis_page():
    """
    Página para análise de cartões de crédito.
    """
    st.title("💳 Análise de Cartão")
    uploaded_file = st.file_uploader(
        "Carregue a imagem do cartão", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file and st.button("💳 Analisar Cartão"):
        result = process_card_analysis(uploaded_file)
        if result:
            card_info, validation_result = result

            st.write("Informações do Cartão:")
            st.write(card_info)

            if validation_result["is_valid"]:
                st.success("✅ Cartão Válido")

                card_info["is_valid"] = validation_result["is_valid"]
                card_info["processed_at"] = datetime.datetime.now().isoformat()
                st.success("Cartão inserido no banco de dados!")
            else:
                st.error("❌ Cartão Inválido")

def main():
    """
    Ponto de entrada para o aplicativo Credit Card Analyzer.

    Página para análise de cartões de crédito.
    """
    
    st.set_page_config(page_title="Credit Card Analyzer", page_icon="💳", layout="wide")
    st.title("💳 Análise de Cartão")
    
    uploaded_file = st.file_uploader(
        "Carregue a imagem do cartão", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file and st.button("💳 Analisar Cartão"):
        result = process_card_analysis(uploaded_file)
        if result:
            card_info, validation_result = result

            st.write("Informações do Cartão:")
            st.write(card_info)

            if validation_result["is_valid"]:
                st.success("✅ Cartão Válido")

                card_info["is_valid"] = validation_result["is_valid"]
                card_info["processed_at"] = datetime.datetime.now().isoformat()
                st.success("Cartão inserido no banco de dados!")
            else:
                st.error("❌ Cartão Inválido")


if __name__ == "__main__":
    main()