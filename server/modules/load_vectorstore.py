import uuid
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from fastapi import HTTPException
from modules.medical_guard import is_medical_text




BASE_DIR = Path(__file__).resolve().parent.parent  
UPLOAD_DIR = BASE_DIR / "uploaded_pdfs"
PERSIST_DIR = BASE_DIR / "chroma_store"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


def load_vectorstore(uploaded_files: List, reset_db: bool = False):
    """
    If reset_db=True, clears the existing Chroma collection before adding new PDFs.
    This ensures Sources always come from PDFs you just uploaded.
    """

    
    vectorstore = Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embed_model,
    )

   
    if reset_db:
        try:
            vectorstore.delete_collection()
        except Exception:
            pass  
        vectorstore = Chroma(
            persist_directory=str(PERSIST_DIR),
            embedding_function=embed_model,
        )

    all_docs = []

    for f in uploaded_files:
        original_name = f.filename

        
        safe_name = f"{uuid.uuid4().hex}.pdf"
        save_path = UPLOAD_DIR / safe_name

        file_bytes = f.file.read()
        with open(save_path, "wb") as out:
            out.write(file_bytes)

        #loader = PyPDFLoader(str(save_path))
        #docs = loader.load()
        loader = PyPDFLoader(str(save_path))
        docs = loader.load()

        
        sample_text = "\n".join(d.page_content for d in docs[:2])

        if not is_medical_text(sample_text):
            
            try:
                save_path.unlink(missing_ok=True)
            except Exception:
                pass

            raise HTTPException(
                status_code=400,
                detail=f"'{original_name}' is not a medical document. MediBot accepts medical PDFs only."
            )


        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        
        for c in chunks:
            c.metadata = c.metadata or {}
            c.metadata["source"] = original_name  
            c.metadata["saved_as"] = safe_name

        all_docs.extend(chunks)

    if all_docs:
        vectorstore.add_documents(all_docs)
        vectorstore.persist()

    print(" CHROMA PERSIST DIR =", str(PERSIST_DIR))
    print(" TOTAL NEW CHUNKS ADDED =", len(all_docs))
