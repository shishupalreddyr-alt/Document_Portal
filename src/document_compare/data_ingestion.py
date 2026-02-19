import sys
from pathlib import Path
import fitz

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class Document_ingestion:
    """Handles the ingestion of documents into the system.
    """
    def __init__(self,base_dir: str ="Data\\Document_compare"):
        """

        Args:
            base_dir (_type_): _description_
        """
        self.log=CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)     
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.log.info("Document ingestion module initialized.")
    
    
    def delete_existing_files(self):
        """Delete existing files in the specified directory.
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info(f"Deleted file: {file.name}")
                self.log.info("All existing files deleted.")
        except Exception as e:
            self.log.error(f"Error occurred while deleting existing files: {e}")
            raise DocumentPortalException(e)

    def save_uploaded_files(self, referenced_file, actual_file):
        """Save uploaded files to the specified directory.
        """
        try:
            self.delete_existing_files()
            self.log.info("Successfully deleted existing files.")

            ref_path= self.base_dir/referenced_file.name
            actual_path= self.base_dir/actual_file.name

            if not referenced_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise DocumentPortalException("Only PDF files are allowed.")

            with open(ref_path, "wb") as f:
                f.write(referenced_file.getbuffer())

            with open(actual_path, "wb") as f:
                f.write(actual_file.getbuffer())
            self.log.info("File saved successfully:", reference=str(ref_path), actual=str(actual_path))
            return ref_path,actual_path

        except Exception as e:
            self.log.error(f"Error occurred while saving uploaded files: {e}")
            raise DocumentPortalException(e)

    def read_pdf(self,pdf_path:Path)->str:
        """Read a PDF document and extract its text content.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted:{pdf_path.name}")
                all_text=[]
                for page_num in range(doc.page_count):
                    page=doc.load_page(page_num)
                    text=page.get_text()

                    if text.strip():
                        all_text.append(f"\n--- Page {page_num + 1} ---\n{text}")

            self.log.info(f"Successfully read PDF: {pdf_path.name}", page_count=doc.page_count)
            return "\n".join(all_text)                         
        except Exception as e:
            self.log.error(f"Error occurred while reading PDF files: {e}")
            raise DocumentPortalException(e)
    
    def combine_documents(self) -> str:
        try:
            content_dict={}
            doc_parts=[]

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix.lower() == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)
                    #text=self.read_pdf(filename)
                    #content_dict[filename.name]=text

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename.name}\n{content}")

            combined_content = "\n".join(doc_parts)
            self.log.info("Successfully combined documents.", count=len(doc_parts))
            return combined_content
        except Exception as e:
            self.log.error(f"Error occurred while combining documents: {e}")
            raise DocumentPortalException(e)