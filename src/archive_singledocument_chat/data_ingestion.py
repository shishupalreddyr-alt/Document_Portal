import uuid
from pathlib  import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
#from pytz import timezone
from datetime import datetime, timezone
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from utils.model_loader import ModelLoader


class SingleDocIngestion:
    def __init__(self,data_dir:str="data/Single_document_chat", faiss_dir:str="faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            
            self.data_dir=Path(data_dir)
            self.faiss_dir=Path(faiss_dir)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.loader = ModelLoader()
            self.log.info("Initializing SingleDocument chat", temp_path=str(self.data_dir),faiss_path=str(self.faiss_dir))

        except Exception as e:
            self.log.error(f"Error occurred during SingleDocIngestion initialization: {e}")
            raise DocumentPortalException(e)

    def ingest_files(self, uploaded_files):
        try:
            documents=[]

            for uploaded_file in uploaded_files:
                unique_filename=f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.pdf"
                temp_path=self.data_dir / unique_filename

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                self.log.info(f"File {uploaded_file.name} saved as {temp_path}")
                loader=PyPDFLoader(str(temp_path)) 
                docs=loader.load()
                documents.extend(docs)
            self.log.info(f"PDF files Loaded {len(documents)} documents")
            return self._create_retreiver(documents) 
            
        except Exception as e:
            self.log.error(f"Error occurred during file ingestion: {e}")
            raise DocumentPortalException(e)

    def _create_retreiver(self,documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(documents)
            self.log.info(f"Documents split into {len(chunks)} chunks")

            embeddings=self.loader.load_embeddings()
            vector_store= FAISS.from_documents(documents=chunks,embedding=embeddings)

        #Save FAISS Index
            vector_store.save_local(str(self.faiss_dir))
            self.log.info(f"FAISS index saved at {self.faiss_dir}")

        #Add retriver as_retreiver 
            retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 5})
            self.log.info("Retriever created successfully")
            return retriever    
        except Exception as e:
            self.log.error(f"Error occurred during retriever creation: {e}")
            raise DocumentPortalException(e)

    