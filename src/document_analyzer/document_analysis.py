import os
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser

import sys 

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from promptengg.promptlibrary import *

class DocumentAnalyzer:
    """Analyzes the content and metadata of documents using pretrained models.
    """
    def __init__(self):
        self.log=CustomLogger().get_logger(__name__)
        try:
            self.model_loader=ModelLoader()
            self.llm=self.model_loader.load_llm()

            #Prepare parsers
            self.parser=JsonOutputParser(pydantic_object=Metadata)
#            self.fixing_parser=OutputFixingParser.from_llm(llm=self.llm, parser=self.parser)

            self.prompt=prompt
            self.log.info("Document analyzer initialized.")

        except DocumentPortalException as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {str(e)}")
            raise DocumentPortalException(e)

    def analyze_metadata(self):
        pass

    def analyze_document(self, document_text: str) -> dict:
        """Analyze the content of a document and extract relevant information.

        Raises:
            DocumentPortalException: If an error occurs during document analysis.

        Returns:
            _type_: _description_
        """
        self.log.info("Analyzing document...")
#        print("llm provider selected:", self.llm)
        try:
            # Use the prompt template for document analysis
            chain=self.prompt | self.llm   #|self.fixing_parser
            self.log.info("Document analysis completed.")
            
            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            
            })
            
            self.log.info("Meta data extraction completed successfully.", keys=list(response.dict().keys()))
            return response
        
        except Exception as e:
            #print("LLM Loaded", self.llm)
            self.log.error(f"Error analyzing document: {str(e)}")
            raise DocumentPortalException(e)


 

