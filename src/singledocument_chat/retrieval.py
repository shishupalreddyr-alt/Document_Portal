import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory,InMemoryChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retreiver,create_retreival_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from promptengg.promptlibrary import PROMPT_REGISTRY
from model.models import *

class ConversationalRAG:
    def __init__(self,session_id:str, retriever) -> None:
        try:
            load_dotenv()
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever = retriever
            self.loader = ModelLoader()
            self.chat_history = InMemoryChatMessageHistory()
            self.vector_store = FAISS()
            self.retriever = create_history_aware_retreiver(self.vector_store, self.chat_history)
            self.chain = create_retreival_chain(self.retriever)
            self.stuff_chain = create_stuff_documents_chain(self.vector_store)  
            
            self.log.info("ConversationalRAG initialized successfully.")
        except Exception as e:
            self.log.error(f"Error initializing ConversationalRAG: {e}")
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error loading LLM: {e}")
            raise DocumentPortalException(e)


    def _get_session_history(self):
        try:
            pass    

        except Exception as e:
            self.log.error(f"Error getting session history: {e}")
            raise DocumentPortalException(e)    
        
    def load_retriever_from_faiss(self):
        try:
            pass    
        except Exception as e:
            self.log.error(f"Error loading retriever from FAISS: {e}")
            raise DocumentPortalException(e)    
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error invoking ConversationalRAG: {e}")
            raise DocumentPortalException(e)    