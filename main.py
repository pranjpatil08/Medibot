from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from modules.load_vectorstore import load_vectorstore
from modules.llm import get_llm_chain
from logger import logger

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
MEDICAL_HINTS = [
    "symptom", "cause", "treatment", "medicine", "medication", "dose", "dosage",
    "doctor", "clinic", "hospital", "diagnos", "risk", "side effect", "infection",
    "virus", "bacteria", "pain", "fever", "throat", "diabetes", "blood", "glucose",
    "antibiotic", "strep", "tonsil", "cough", "cold"
]

EMERGENCY_HINTS = [
    "chest pain", "trouble breathing", "can't breathe", "shortness of breath",
    "stroke", "face drooping", "slurred speech", "severe bleeding", "fainting",
    "unconscious", "seizure", "suicidal", "overdose"
]


embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

app = FastAPI(title="RagBot2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})

@app.get("/")
async def root():
    return {"message": "RagBot2.0 backend is running. Go to /docs"}

@app.get("/test")
async def test():
    return {"message": "Testing successful..."}

@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"received {len(files)} files")
        load_vectorstore(files, reset_db=True)

        return {"message": "Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask/")
async def ask_question(
    question: str = Form(...),
    selected_pdf: str = Form(None),
):
    try:
        logger.info(f"user query: {question} | selected_pdf={selected_pdf}")

        BASE_DIR = Path(__file__).resolve().parent
        PERSIST_DIR = BASE_DIR / "chroma_store"

        vectorstore = Chroma(
            persist_directory=str(PERSIST_DIR),
            embedding_function=embed_model,
        )

        
        search_kwargs = {"k": 12}

        if selected_pdf:
            search_kwargs["filter"] = {"source": selected_pdf}

        q_lower = question.lower()
        
        if not any(h in q_lower for h in MEDICAL_HINTS) and not selected_pdf:
            return {
                "response": "I’m MediBot, a medical document assistant. Please ask a medical question related to your uploaded PDFs.",
                "sources": [],
            }

        
        if any(h in q_lower for h in EMERGENCY_HINTS):
            return {
                "response": "Your message may describe an urgent medical situation. Please seek immediate medical care or call your local emergency number. If you want, you can also ask me to summarize what your uploaded documents say about these symptoms.",
                "sources": [selected_pdf] if selected_pdf else [],
            }

        if "title" in q_lower or "document title" in q_lower:
            if selected_pdf:
                search_kwargs["filter"] = {
                    "$and": [
                        {"source": selected_pdf},
                        {"page": 0}
                    ]
                }
            else:
                search_kwargs["filter"] = {"page": 0}

        retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
        chain = get_llm_chain(retriever)

        raw = chain.invoke({"query": question})

        
        sources, seen = [], set()
        for d in raw.get("source_documents", []):
            src = d.metadata.get("source", "")
            page = d.metadata.get("page", None)
            key = (src, page)
            if src and key not in seen:
                seen.add(key)
               
                if isinstance(page, int):
                    sources.append(f"{src} (page {page + 1})")
                else:
                    sources.append(src)


        return {
            "response": raw.get("result", ""),
            "sources": sources,
        }

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/sources")
async def list_sources():
    BASE_DIR = Path(__file__).resolve().parent
    PERSIST_DIR = BASE_DIR / "chroma_store"

    vectorstore = Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embed_model)
    data = vectorstore.get(include=["metadatas"])

    all_sources = []
    for md in data.get("metadatas", []):
        if md and md.get("source"):
            all_sources.append(md["source"])

    return {"pdfs_in_db": sorted(set(all_sources))}

@app.get("/debug_sample")
async def debug_sample(selected_pdf: str = Query(None), n: int = Query(5)):
    BASE_DIR = Path(__file__).resolve().parent
    PERSIST_DIR = BASE_DIR / "chroma_store"

    vectorstore = Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embed_model,
    )

    data = vectorstore.get(include=["documents", "metadatas"])

    docs = data.get("documents", [])
    mds = data.get("metadatas", [])

    samples = []
    for doc, md in zip(docs, mds):
        if selected_pdf and md.get("source") != selected_pdf:
            continue
        samples.append({
            "source": md.get("source"),
            "page": md.get("page"),
            "text_preview": (doc[:300] if doc else "")
        })
        if len(samples) >= n:
            break

    return {"samples": samples}
