import io
from pathlib import Path
from src.document_compare.data_ingestion_01 import Document_ingestion
from src.document_compare.document_comparator import DocumentComparatorLLM


def load_fake_uploaded_file(file_path: Path):
    #return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()
    return file_path.read_bytes()  # simulate .getbuffer()

def test_compare_documents():
    #ref_path = Path("C:\\LLMOpSProjects\\Document_Portal\\Data\\Document_compare_files\\GENAI RAG Interview Questions.pdf")
    #act_path = Path("C:\\LLMOpSProjects\\Document_Portal\\Data\\Document_compare_files\\Mastering-RAG.pdf.pdf")

    ref_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\GENAI RAG Interview Questions.pdf"
    act_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\Mastering-RAG.pdf"

    class FakeUpload:
        def __init__(self, file_path):
    #        self.name = file_path.name
    #       self._buffer = load_fake_uploaded_file(file_path)
            self.name = Path(file_path).name
            self._file_path = file_path

        def getbuffer(self):
            return open(self._file_path, "rb").read()
#  
            #return self._buffer

    Doc_comparator = Document_ingestion()

    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    ref_file,act_file = Doc_comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text=Doc_comparator.combine_documents()

    print("Combined Text:", combined_text[:500])  # Print the first 500 characters to verify


    llm_compare = DocumentComparatorLLM()
    compare_df=llm_compare.document_comparator(combined_text)
    #comparison_result = llm_compare.document_comparator(combined_text)
    print("LLM Comparison Result:", compare_df.head())  # Print the first few rows of the comparison result DataFrame


if __name__ == "__main__":
    test_compare_documents()
