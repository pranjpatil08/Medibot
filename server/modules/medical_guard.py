import re

MEDICAL_KEYWORDS = [
    "symptom", "symptoms", "diagnosis", "diagnosed", "treatment", "treat", "therapy",
    "medication", "medicine", "dose", "dosage", "side effect", "contraindication",
    "clinical", "patient", "doctor", "physician", "hospital", "urgent", "emergency",
    "infection", "virus", "bacteria", "antibiotic", "inflammation", "fever",
    "pain", "throat", "cough", "rash", "swelling", "blood", "pressure",
    "diabetes", "cancer", "asthma", "allergy", "vaccine", "surgery"
]

NON_MED_HINTS = [
    "information retrieval", "tf-idf", "bm25", "precision", "recall", "ranking",
    "dataset", "algorithm", "evaluation", "neural network", "transformer",
    "architecture", "github", "compiler", "operating system"
]

def is_medical_text(text: str) -> bool:
    t = (text or "").lower()
    t = re.sub(r"\s+", " ", t)

    med_hits = sum(1 for k in MEDICAL_KEYWORDS if k in t)
    nonmed_hits = sum(1 for k in NON_MED_HINTS if k in t)

    return (med_hits >= 3) and (nonmed_hits <= 2)
