from pathlib import Path
from typing import Tuple, List

import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    """
    Handles document saving, validation, and PDF text extraction.
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

    # ----------------------------------------------------
    # File Management
    # ----------------------------------------------------

    def delete_existing_files(self) -> None:
        """Delete existing files in the base directory."""
        for file in self.base_dir.glob("*"):
            if file.is_file():
                file.unlink()

        if self.log:
            self.log.info("Existing files deleted successfully.")

    def save_uploaded_files(self, referenced_file, actual_file):
        """
        Save uploaded PDF files to base directory.
        """
        try:
            self.delete_existing_files()

            self._validate_pdf(referenced_file.name)
            self._validate_pdf(actual_file.name)

            ref_path = self.base_dir / referenced_file.name
            actual_path = self.base_dir / actual_file.name

            self._write_file(ref_path, referenced_file._getbuffer())
            self._write_file(actual_path, actual_file._getbuffer())

            if self.log:
                self.log.info(f"Files saved: {ref_path}, {actual_path}")

            return ref_path, actual_path

        except Exception as e:
            if self.log:
                self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException(e)

    def _write_file(self, path: Path, content: bytes) -> None:
        """Write bytes to file safely."""
        with open(path, "wb") as f:
            f.write(content)

    def _validate_pdf(self, filename: str) -> None:
        """Validate that file is a PDF."""
        if not filename.lower().endswith(".pdf"):
            raise DocumentPortalException("Only PDF files are allowed.")

    # ----------------------------------------------------
    # PDF Reading
    # ----------------------------------------------------

    def read_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file using PyMuPDF.
        """
        try:
            if not pdf_path.exists():
                raise FileNotFoundError(f"File not found: {pdf_path}")

            all_text: List[str] = []

            with fitz.open(str(pdf_path)) as doc:
                if doc.is_encrypted:
                    raise DocumentPortalException(
                        f"PDF is encrypted: {pdf_path.name}"
                    )

                page_count = doc.page_count

                for page_num in range(page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()

                    if text.strip():
                        all_text.append(
                            f"\n--- Page {page_num + 1} ---\n{text}"
                        )

            if self.log:
                self.log.info(
                    f"Successfully read {pdf_path.name} | Pages: {page_count}"
                )

            return "\n".join(all_text)

        except Exception as e:
            if self.log:
                self.log.error(f"Error reading PDF {pdf_path.name}: {e}")
            raise DocumentPortalException(e)

    # ----------------------------------------------------
    # Document Combination
    # ----------------------------------------------------

    def combine_documents(self, ref_path: Path, actual_path: Path) -> str:
        """
        Combine two PDFs into a structured comparison string.
        """
        try:
            print("ref path:", ref_path, "act path:", actual_path)

            ref_text = self.read_pdf(ref_path)
            actual_text = self.read_pdf(actual_path)

            combined_text = (
                "\n================ REFERENCE DOCUMENT ================\n"
                + ref_text
                + "\n\n================ ACTUAL DOCUMENT ====================\n"
                + actual_text
            )

            if self.log:
                self.log.info("Documents combined successfully.")

            return combined_text

        except Exception as e:
            if self.log:
                self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException(e)
