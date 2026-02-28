import os

from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.base import RunnableMap,Runnable
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from promptengg.promptlibrary import PROMPT_REGISTRY
from langchain_core.output_parsers import StrOutputParser
from model.models import PromptType
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from typing import List,Optional
from langchain_core.messages import BaseMessage



class ConversationalRAG:
    def __init__(self,session_id:str, retriever=None):

        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id=session_id
            self.llm= self.load_llm()

            self.contextualize_prompt:ChatPromptTemplate =PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt : ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]

            if retriever is None:
                raise ValueError("Retreiver is not found")
            self.retriever = retriever

            self._build_lcel_chain()
            self.log.info("Conv RAG initialized", session_id = self.session_id)

        except Exception as e:
            self.log.error(f"Failed to initialize Conv RAG: str{e}")
            raise DocumentPortalException(e)
        

    def load_retriever_from_faiss(self,index_path:str):
        try:
            embeddings = ModelLoader().load_embeddings
            if not os.path.isdir(index_path):
                raise FileNotFoundError("FAISS Index directry not found: {index_path}")
            
            vectorstore=FAISS.load_local(
                index_path,
                embeddings,
                allow_dangarous_deserialization=True
            )
            self.retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})
            self.log.info("FAISS retriever loaded successfully",index_path=index_path,session_id=self.session_id)

            #self._build_lcel_chain()
            return self.retriever

        except Exception as e:
            self.log.error(f"Failed to read from FAISS: {e}")
            
            raise DocumentPortalException(e)
            

    def invoke(self, user_input : str,chat_history: Optional[List[BaseMessage]]= None) ->str:
        """_summary_

        Args:
            user_input (str): _description_
            chat_history (Optional[list[BaseMessage]], optional): _description_. Defaults to None.

        Raises:
            DocumentPortalException: _description_

        Returns:
            str: _description_
        """
        try:
            chat_history=chat_history or []
            payload={"input": user_input, "chat_history" : chat_history }
            answer=self.chain.invoke(payload)
            if not answer:
                self.log.warning("No anwere generated", user_input=user_input,session_id=self.session_id)
                return "No answer"
            self.log.info("Chain invoked successfully",
                        session_id=self.session_id,
                        user_input=user_input,
                        answer_preview=answer[:50]
                        )
            return answer    
        except Exception as e:
            self.log.error(F"Failed to invoke Conv RAG: str{e}")
            raise DocumentPortalException(e)
            

    def load_llm(self):
        try:
            llm=ModelLoader().load_llm

            if not llm:
                raise ValueError("LLM could not be loaded")
            self.log.info("LLM loaded successfully",session_id=self.session_id)
            return llm
        except Exception as e:
            self.log.error(f"Failed to load LLM:str{e}")
            raise DocumentPortalException(e)


    @staticmethod
    def _format_doc(docs):
        try:
            return "\n""\n".join(d.page_content for d in docs)
        
        except Exception as e:
            #self.log.error(f"Failed to load LLM: str{e}")
            raise DocumentPortalException(e)
    
    def _build_lcel_chain(self,):
        try:
            question_rewriter = (
                {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
                |self.contextualize_prompt
                |self.llm
                |StrOutputParser
            )
            retrieve_docs= self.retriever | self._format_doc
            
            self.chain=(
                {
                    "context": retrieve_docs,
                    "input": itemgetter("input"),
                    "chat_history": itemgetter("chat_history"),

                }
                |self.qa_prompt
                |self.llm
                |StrOutputParser
            )

            self.log.info("LCEL Sequential chain is done", session_id= self.session_id)
        except Exception as e:
            self.log.error(f"Failed to build RAG Chain :str{e}")
            raise DocumentPortalException(e)
        
