from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request # type: ignore
from fastapi.responses import JSONResponse,HTMLResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore

from typing import List, Optional, Any, Dict
import os

from src.document_ingestion.data_ingestion import (
    DocumentHandler,
    DocumentCompare,
    ChatIngestor,
    FaissManager)
from src.document_analyzer.document_analysis import DocumentAnalyzer
from src.document_compare.document_comparator import DocumentComparatorLLM
from src.document_chat.retrieval import ConversationalRAG

#from langchain_community.vectorstores import FAISS  #typeignore 


app = FastAPI(title="Document Portal API", version="0.1")
app.add_middleware(CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
                )

#app.mount("/static", StaticFiles(directory="../static"),name="static")
#templates = Jinja2Templates(directory="../templates")

#app.mount("/static", StaticFiles(directory="static"), name="static")
#templates = Jinja2Templates(directory="templates")

# Mount static folder
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../static")), name="static")

# Set templates folder
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../templates"))


@app.get("/", response_class=HTMLResponse)
async def serve_ui(request:Request):

    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "document_portal"}

class FastAPIFileAdapter:
    def __init__(self,uf:UploadFile):
        self._uf=uf
        self.name=uf.filename

    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()
    
def _read_pdf_via_handler(handler:DocumentHandler, path:str) ->str:
    pass

@app.post("/analyze")
async def anlyze_document(file:UploadFile = File(...)) -> Any:
    try:
        dh=DocumentHandler()
        save_path=dh.save_pdf(FastAPIFileAdapter(file))
        text=_read_pdf_via_handler(dh,save_path)

        analyzer=DocumentAnalyzer()
        result=analyzer.analyze_document(text)
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")


@app.post("/compare")
async def compare_documents(file:UploadFile = File(...)) -> Any:
    try:
        dc=DocumentCompare()
        ref_path, act_path=dc.save_uploaded_file(FastAPIFileAdapter(reference),FastAPIFileAdapter(actual))
        _= ref_path, act_path
        combinedtext=dc.combine_documents()
        comp=DocumentComparatorLLM()
        df=comp.document_comparator(combinedtext)
        return.{"rows:df.to_dict(orient="records), "sesion_id":dc.session_id"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")

@app.post("/chat/index")
async def chat_build_index(
    files:List[UploadFile] = File(...),
    session_id:Optional[str]=Form(None),
    use_session_dirs:bool=Form(True),
    chunk_size:int=Form(400),
    chunk_overlap :int  =Form(100),
    k:int = Form(5)) -> Any:
    try:
        wrapped = [FastAPIFileAdapter(f) for f in files]

        ci=ChatIngestor(
            temp_base=UPLOAD_BASE,
            faiss_base= FAISS_BASE,
            use_sessions_dirs=use_session_dirs,
            session_id=session_id or None,

        )
        ci.built_retreiver(wrapped, chunk_size=chunk_size,chunk_overlap=chunk_overlap,k=k)

    except HTTPException:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")



@app.post("/chat/query")
async def chat_query(
    question: str = Form(...),
    session_id: Optional[str] = Form(None),
    use_session_dirs: bool = Form(True),
    k: int = Form(5),
) -> Any:
    try:
        #log.info(f"Received chat query: '{question}' | session: {session_id}")
        if use_session_dirs and not session_id:
            raise HTTPException(status_code=400, detail="session_id is required when use_session_dirs=True")

        index_dir = os.path.join(FAISS_BASE, session_id) if use_session_dirs else FAISS_BASE  # type: ignore
        if not os.path.isdir(index_dir):
            raise HTTPException(status_code=404, detail=f"FAISS index not found at: {index_dir}")

        rag = ConversationalRAG(session_id=session_id)
        rag.load_retriever_from_faiss(index_dir, k=k, index_name=FAISS_INDEX_NAME)  # build retriever + chain
        response = rag.invoke(question, chat_history=[])
        #log.info("Chat query handled successfully.")

        return {
            "answer": response,
            "session_id": session_id,
            "k": k,
            "engine": "LCEL-RAG"
        }
    except HTTPException:
        raise
    except Exception as e:
        #log.exception("Chat query failed")
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
### uvicorn api.main:app --reload    command to test fast API 