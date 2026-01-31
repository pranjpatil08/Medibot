# server/modules/llm.py

import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

from logger import logger

load_dotenv()


def get_llm_chain(retriever):
    """
    Builds a RetrievalQA chain using the given retriever.
    The retriever must be a LangChain retriever (implements relevant document retrieval).
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to server/.env")

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    logger.info(f"Using Groq model: {model}")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model=model,
        temperature=0.2,
    )

    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are **MediBot**, a medical document assistant.

You MUST answer using ONLY the provided Context from the user's uploaded medical PDFs.
Do NOT use outside knowledge.

CRITICAL RULE:
- If the user's question is NOT answered anywhere in the Context,
  respond with EXACTLY this single sentence (and nothing else):
  "This information is not specified in the uploaded medical document."

Safety rules:
- You are NOT a doctor. Do NOT diagnose. Do NOT prescribe medication or give exact dosages.
- If the user asks for dosage, drug interaction, or “should I take”, respond with what the document says (if present) and advise consulting a clinician/pharmacist.
- If the user describes emergency symptoms (chest pain, trouble breathing, severe bleeding, stroke signs, fainting), advise urgent medical care.

When the answer IS present in the Context, use this format:
1) **What the document says (summary)**: 3–6 bullets
2) **Key details**: short paragraph (only from context)
3) **When to seek medical care (if mentioned)**: bullets (only if present in context; otherwise say “Not specified in the document.”)
4) **Questions to ask a doctor**: 3 bullets
5) **Sources used**: state that the answer is based on the provided document context

Context:
{context}

Question:
{question}

Answer:
""".strip(),
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return chain
