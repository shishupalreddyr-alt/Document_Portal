import os
import fitz  # wrapper on top of pypdg loader 
import uuid
from datetime import datetime

from logger.custom_logger import CustomLogger

from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """Handles document processing tasks. Save, Read operations on PDF documents.
    Automatic logging of all actions and support session based organization.
    this enables Data versioning
    """
    def __init__(self):
        pass

    def save_pdf(self):
        pass

    def read_pdf(self):
        pass

    
