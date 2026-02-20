from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM


class FakeUpload:
    def __init__(self, file_path: Path):
        self.name = file_path.name
        self._buffer = file_path.read_bytes()

    def getbuffer(self):
        return self._buffer


def test_compare_documents():

    #base_dir = r"Data\Document_compare"

    #ingestion = DocumentIngestion(base_dir=base_dir)

    ref_path = Path("C:\\LLMOpSProjects\\Document_Portal\\Data\\Document_compare\\GENAIRAGInterviewQuestions.pdf")
    act_path = Path("C:\\LLMOpSProjects\\Document_Portal\\Data\\Document_compare\\MasteringRAG.pdf")

#ref_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\GENAI RAG Interview Questions.pdf"
#    act_path = r"C:\LLMOpSProjects\Document_Portal\Data\Document_compare\Mastering-RAG.pdf"

    class FakeUpload:
        def __init__(self, file_path: Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()

    def getbuffer(self):
        return self._buffer
    
    ingestion = DocumentIngestion()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    ref_file, act_file = ingestion.save_uploaded_files(ref_upload, act_upload)
    
    print("ref file:", ref_file, "act file:", act_file)

    combined_text = ingestion.combine_documents(ref_file, act_file)

    llm_compare = DocumentComparatorLLM()
    compare_df = llm_compare.document_comparator(combined_text)

    print(compare_df.head())


if __name__ == "__main__":
    test_compare_documents()
