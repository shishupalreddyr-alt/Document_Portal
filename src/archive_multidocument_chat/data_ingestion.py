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



class DocumentIngestor:
    SUPPORTED_FILE_TYPES= {'.pdf', '.doc', '.docx', '.txt','.md', '.ppt', '.pptx'}

    def __init__(self, temp_dir : str = "data/multidocument_chat",faiss_dir:str="faiss_index",session_id:str | None=None):
        try:
            self.log= CustomLogger().get_logger(__name__)


            ##Base dirs
            self.temp_dir=Path(temp_dir)
            self.faiss_dir=Path(faiss_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            ##Sessionized paths
            self.session_id= session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir=self.temp_dir / self.session_id
            self.session_faiss_dir=self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()
            self.log.info(
                "DocumentIngestor initialized",
                temp_base=str(self.temp_dir),
                temp_faiss=str(self.faiss_dir),
                session_id=self.session_id,
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir)

            )
            
        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", {e})
            raise DocumentPortalException(e)

            

    def ingest_files(self, uploaded_files):
        try:
            documents=[]

            for uploaded_file in uploaded_files:
                ext=Path(uploaded_file.name).suffix.lower()
                if ext not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning("Unsupported files skipped", filename=uploaded_file.name)

                unique_filename= "Testing123"#f"{uuid:uuid4().hex[:8]{ext}}"
                temp_path= self.session_temp_dir / unique_filename

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                self.log.info("File savd for ingestion", filename=uploaded_file.name, saved_as=str(temp_path),sessions_id=self.session_id)

                if ext==".pdf":
                    loader=PyPDFLoader(str(temp_path))
                elif ext == ".docx":
                    loader= Docx2txtLoader(str(temp_path))
                elif ext ==".txt":
                    loader=TextLoader(str(temp_path), encoding="utf-8")
                else:
                    self.log.warning("Unsupported file type ", filename=uploaded_file.name)

                docs= loader.load()
                documents.extend(docs)

            if not documents:
                raise ValueError("error")
        
            self.log.info("All documents loaded", total_doc_len=len(documents),session_id=self.session_id)
            return self._create_retriever(documents)          
        except Exception as e:
            self.log.error(f"Error occurred during file ingestion: {e}")
            raise DocumentPortalException(e)

    def _create_retriever(self,documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            chunks = splitter.split_documents(documents)

            self.log.info("Document split into chunks", total_chunks=len(chunks),session_id=self.session_id)
            embeddings = self.model_loader.load_embeddings()
            #print("embeddings", embeddings)
            vectorstore= FAISS.from_documents(documents=chunks,embedding=embeddings)

            vectorstore.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS Index saved to disk", path=str(self.session_faiss_dir),session_id=self.session_id)

            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})

            self.log.info("FAISS retreiver created and ready to use", session_id= self.session_id)
            return retriever

        except Exception as e:
            self.log.error(f"Error occurred during retreival: {e}")
        
            raise DocumentPortalException(e)
                
        