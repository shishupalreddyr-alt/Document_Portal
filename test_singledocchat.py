import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from src.singledocument_chat.data_ingestion import SingleDocIngestion
from src.singledocument_chat.retrieval import ConversationalRAG
from utils.model_loader import ModelLoader

FAISS_INDEX_PATH = Path("faiss_index")

def test_conv_rag(pdf_path:str,question:str):
    try:
        model_loader=ModelLoader()
        if FAISS_INDEX_PATH.exists():
            print("FAISS index already exists. Loading existing index.")
            embeddings=model_loader.load_embeddings()
            vector_store=FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)
            retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 5} )
        else:
            print("FAISS index not found. Ingesting PDF and creating INDEX")
            with open(pdf_path, "rb") as f:
                uploaded_file = [f]
                ingestor=SingleDocIngestion()
                retriever=ingestor.ingest_files(uploaded_file)
        print("Running Conversational RAG....")     
        session_id="test_conv_rag"
        rag=ConversationalRAG(retriever=retriever, session_id=session_id)
        response=rag.invoke(question)
        print(f"\nQuestion:{question}\nAnswer:{response}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    pdf_path = "C:\\LLMOpSProjects\\Document_Portal\\Data\\Single_document_chat\\MasteringRAG.pdf"
    question = "What are the key chunking methods in RAG"

    if not Path(pdf_path).exists():
        print(f"PDF file does not exist: {pdf_path}")
        sys.exit(1)

    test_conv_rag(pdf_path, question)
