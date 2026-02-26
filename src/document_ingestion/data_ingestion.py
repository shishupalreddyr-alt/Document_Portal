
from __future__ import annotations   #used for circular import, future referening etc 
import os
import sys
import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable, List, Optional, Dict, Any

import fitz
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loader import PyPDFLoader, Doc2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from utils.file_io import _session_id, save_uploaded_file
from utils.document_ops import load_documents, concat_for_analysis, concat_for_comparison




class FaissManager:
    """_summary_
    """
    def __inti__(self):
        pass

    
    def _exists(self):
        pass

    @staticmethod
    def  _fingerprint():
        pass

    def _save_metadata(self):
        pass

    def add_documents(self):
        pass

    def load_or_create(self):
        pass

class DocumentHandler:
    """_summary_
    """
    def __init(self):
        pass

    def save_pdf(self):
        pass

    def read(pdf):
        pass


class DocumentCompare:
    """
    
    """
    def __init__(self):
        pass

    def save_uploaded_file(self):
        pass


    def read_pdf(self):
        pass

    def combine_documents(self):
        pass

    def clean_old_session(self):
        pass



class ChatIngestor:
    
    def __init__(self):
        pass

    def _resolve_dir(self):
        pass

    def _split(self):
        pass

    def built_retreiver(self):
        pass
    


