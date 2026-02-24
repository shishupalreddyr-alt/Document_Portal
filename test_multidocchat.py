import sys
from pathlib import Path
from src.multidocument_chat.data_ingestion import DocumentIngestor
from src.multidocument_chat.retrieval import ConversationalRAG

def test_document_ingestion_rag():
    try:
        test_files=[
            "Data\\Multi_document_chat\\GENAIRAGInterviewQuestions.pdf"
            "Data\\Multi_document_chat\\MasteringRAG.pdf"
        ]

        uploaded_files=[]
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"file does not exists")
        if not uploaded_files:
            print(f"No valid files")
            sys.exit(1)            

## Data ingestion
        ingestor=DocumentIngestor()
        retriever=ingestor.ingest_files(uploaded_files)

        for f in uploaded_files:
            f.close()

##Retreival
        session_id="test_multidocchat"
        rag=ConversationalRAG(session_id=session_id,retriever=retriever)
        question = "What are key RAG Metrics"

        answer=rag.rag.invoke(question)
        print("\n Question:", question)
        print("\n answer" , answer)


        
    except Exception as e:
        print("Test failed": {str(e)})
        sys.exit(1)


        