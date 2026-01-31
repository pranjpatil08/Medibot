import requests
from config import API_URL


def upload_pdfs_api(files):
    files_payload = [("files", (f.name, f.read(), "application/pdf")) for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)


def ask_question(question, selected_pdf=None):
    payload = {"question": question}
    if selected_pdf:
        payload["selected_pdf"] = selected_pdf
    return requests.post(f"{API_URL}/ask/", data=payload)


def safe_message(response):
    """
    Extract a readable message from FastAPI responses.
    Works for:
    - {"detail": "..."}
    - {"error": "..."}
    - plain text
    """
    try:
        data = response.json()
        if isinstance(data, dict):
            return data.get("detail") or data.get("error") or str(data)
        return str(data)
    except Exception:
        return response.text
