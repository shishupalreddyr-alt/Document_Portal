import os
import fitz  # wrapper on top of pypdf loader
import uuid
from datetime import datetime

from logger.custom_logger_archive2 import CustomLogger

from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """Handles document processing tasks. Save, Read operations on PDF documents.
    Automatic logging of all actions and support session based organization.
    this enables Data versioning
    """
    def __init__(self,data_dir=None,session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__)

            self.data_dir=data_dir or os.getenv(
                "DATA_STORAGE_PATH",  
                os.path.join(os.getcwd(),"data","document_analysis" )
            )
                ### Session ID will be unique for each user interaction
            self.session_id=session_id or f"sessions_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"  
                ###Create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)   

            self.log.info(f"Session directory created for DATA Storage: {self.session_id}, {self.session_path}")
        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {str(e)}")
            raise DocumentPortalException("Error initializing DocumentHandler",e) from e
        
    
    
    def save_pdf(self,uploaded_file):
        try:
            filename=os.path.basename(uploaded_file.name)

            if not filename.lower().endswith('.pdf'):
                self.log.error(f"Invalid file type: {str(e)}")
                raise DocumentPortalException("Uploaded file is not a PDF")
            save_path=os.path.join(self.session_path,filename)
            
            with open(save_path,"wb") as f:
                #with open(uploaded_file,"rb") as src_file:
                f.write(uploaded_file.getbuffer()) 
            self.log.info(f"PDF saved successfully at {save_path}")
            return save_path
        except DocumentPortalException as e:
            self.log.error(f"Error saving PDF: {str(e)}")
            raise DocumentPortalException(f"Error saving PDF:{str(e)}",e) from e

    def read_pdf(self):
        try:
            pass
        except DocumentPortalException as e:
            self.log.error(f"Error reading PDF: {str(e)}")
            raise DocumentPortalException("Error reading PDF", e) from e    



### Testing DocumentHandler with Exception handling

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
#    try:
    doc_handler = DocumentHandler()
    pdf_path="C:\\LLMOpSProjects\\Document_Portal\\Data\\Document_analysis\\SAP Joule Nov 2025.pdf"
    doc_handler.save_pdf(pdf_path)
#    except DocumentPortalException as e:
#   print("Custom Exception Caught:")
#  print(e)

    class DummyFile:
        def __init__(self, file_path):
            self.name=Path(file_path).name
            self._file_path_=file_path
            

        def getbuffer(self):
            
            return open(self._file_path_,"rb").read()

    dummy_pdf = DummyFile(pdf_path)

    handler=DocumentHandler(session_id="Testsesion")

    try:
        saved_path=handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")

    except DocumentPortalException as e:
        print("Custom Exception Caught:")
        print(e)
        #raise DocumentPortalException("Error occurred in DocumentHandler", e) from e
