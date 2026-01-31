# Medibot🩺
MediBot is a domain-specific medical document intelligence system that enables patients, students, and healthcare professionals to interactively query medical PDFs and receive accurate, context-grounded answers strictly sourced from their documents.

We’ve all opened a medical report and felt this:

pages of clinical terms

long paragraphs

numbers we don’t understand

and no clear answers

You shouldn’t be in a dilemma to understand your own health information.

So I built MediBot.🩺

1 Upload your reports

2 Ask questions naturally

3 Get answers only from your documents

Nothing invented.

Nothing guessed.

Just clarity.

✨Features:
1. Multi-PDF Upload📄: Upload multiple medical files at once.
2. Semantic Search🔍: Finds relevant information even if wording differs.
3. Conversational Q&A 💬: Ask questions naturally.
4. Source Citation📌: Shows where the answer came from.
5. Safety Guardrails🛡: Rejects non-document or diagnostic questions.
6. Domain-Specific Behavior🧠: Built specifically for healthcare documents.
       # 🏗 Architecture

```
        🖥 User UI (Streamlit)
                    │
                    ▼
          ⚡ FastAPI Backend
                    │
                    ▼
        📄 PDF Loader & Text Splitter
                    │
                    ▼
        🧠 Embeddings (Sentence-BERT)
                    │
                    ▼
        📦 Vector Store (ChromaDB)
                    │
                    ▼
        🔎 Retriever
                    │
                    ▼
        🤖 LLM
                    │
                    ▼
        ✅ Answer + Sources
```



✨Technical Stack:
1. Backend API: Built with FastAPI
2. Frontend: Built with Streamlit
3. LangChain
4. Embeddings (SentenceTransformers)
5. ChromaDB (Vector Database)

✨Installation

git clone <repo-url>

cd MediBot

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
