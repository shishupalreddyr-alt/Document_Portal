import uuid
from pathlib  import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from utils.model_loader import ModelLoader


class SingleDocIngestion:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.loader = ModelLoader()
            self.pdf_loader=PyPDFLoader()
            self.text_splitter = RecursiveCharacterTextSplitter()
            self.vector_store = FAISS()
            self.document = None
        except Exception as e:
            self.log.error(f"Error occurred during SingleDocIngestion initialization: {e}")
            raise DocumentPortalException(e)

    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred during file ingestion: {e}")
            raise DocumentPortalException(e)

    def _create_retreiver(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred during retriever creation: {e}")
            raise DocumentPortalException(e)

    