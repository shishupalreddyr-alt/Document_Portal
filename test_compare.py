import io
from pathlib import Path
from src.document_compare.old_data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM


def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()
    #return file_path.read_bytes()  # simulate .getbuffer()

def test_compare_documents():
    ref_path = Path(r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\GENAIRAGInterviewQuestions.pdf")
    act_path = Path(r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\MasteringRAG.pdf")
# BASE_DIR = Path(__file__).resolve().parent

    #data_folder = BASE_DIR / "Data" / "Document_compare"

    #ref_path = data_folder / "GENAIRAGInterviewQuestions.pdf"
    #act_path = data_folder / "MasteringRAG.pdf"

    print("Reference exists:", ref_path.exists())
    print("Actual exists:", act_path.exists())
    
    if not ref_path.exists():
        raise FileNotFoundError(f"Reference file not found: {ref_path}")

    if not act_path.exists():
        raise FileNotFoundError(f"Actual file not found: {act_path}")
    
    #ref_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\GENAI RAG Interview Questions.pdf"
    #act_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\Mastering-RAG.pdf"

    class FakeUpload:
        def __init__(self, file_path:Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()
    
    #       self.name = Path(file_path).name
    #       self._file_path = file_path

        def getbuffer(self):
        # return open(self._file_path, "rb").read()
#  
            return self._buffer

    Doc_comparator = DocumentIngestion()

    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    ref_file, act_file = Doc_comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = Doc_comparator.combine_documents(ref_file, act_file)

    print("Combined Text:", combined_text[:500])  # Print the first 500 characters to verify


    llm_compare = DocumentComparatorLLM()
    compare_df=llm_compare.document_comparator(combined_text)
    comparison_result = llm_compare.document_comparator(combined_text)
    print("LLM Comparison Result:", compare_df.head())  # Print the first few rows of the comparison result DataFrame


if __name__ == "__main__":
    test_compare_documents()
