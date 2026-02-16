import sys
from dotenv import load_dotenv
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from promptengg.promptlibrary import PROMPT_REGISTRY
from model.models import *
from utils.model_loader import ModelLoader


class DocumentComparatorLLM:
    def __init__(self):
        load_env=load_dotenv()
        self.log=CustomLogger().get_logger(__name__)
        self.loader=ModelLoader()
        self.llm=self.loader.load_llm()
        self.parser=JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser=OutputFixingParser.from_llm(llm=self.llm, parser=self.parser)
        self.prompt=PROMPT_REGISTRY["document_comparison"]
        self.chain=self.prompt | self.llm | self.parser | self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized successfully.")

    def document_comparator(self):
        """Compares two documents and returns the differences.

        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred during document comparison: {e}")
            raise DocumentPortalException(e)

    def _format_response(self):
        """Formats the response from the document comparison.

        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error for formatting response: {e}")
            raise DocumentPortalException(e)