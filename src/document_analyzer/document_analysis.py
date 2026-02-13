import os
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser  
#from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import OutputFixingParser 
import sys 

from logger.custom_logger_archive2 import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *


class DocumentAnalyzer:
    """Analyzes the content and metadata of documents using pretrained models.
    """
    def __init__(self):
        self.log=CustomLogger().get_logger(__name__)
        try:
            self.model_loader=ModelLoader()
            self.llm=self.model_loader.load_llm("llm")

            self.metadata_model=self.model_loader.load_model("metadata_extractor")
            self.document_model=self.model_loader.load_model("document_analyzer")
        except DocumentPortalException as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {str(e)}")
            raise DocumentPortalException("Error initializing DocumentAnalyzer", e) from e

    def analyze_metadata(self):
        pass

    def analyze_document(self):
        pass




 

