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
        pass

    def document_comparator(self):
        """Compares two documents and returns the differences.

        """
        pass

    def _format_response(self):
        """Formats the response from the document comparison.

        """
        pass
    