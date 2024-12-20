import re

URGENT_KEYWORDS = [
    "chest pain", "severe bleeding", "shortness of breath", 
    "unconscious", "heart attack", "stroke", "call 911", "difficulty breathing", "no pulse", "severe allergic reaction"
]

SENSITIVE_KEYWORDS = [
    "suicidal", "overdose", "self-harm", "child abuse", "domestic violence", "sexual assault"
]

DISCLAIMER_TEXT = (
    "\n\n**Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice."
    " Always consult a healthcare provider for diagnosis and treatment recommendations."
)

def needs_urgent_escalation(text):
    """Returns True if user query likely indicates a medical emergency."""
    normalized = text.lower()
    return any(kw in normalized for kw in URGENT_KEYWORDS)

def is_sensitive_topic(text):
    """Returns True if the query is related to sensitive topics needing careful handling."""
    normalized = text.lower()
    return any(kw in normalized for kw in SENSITIVE_KEYWORDS)

def append_disclaimer(answer):
    """Appends a medical disclaimer to the answer, if not already present."""
    if DISCLAIMER_TEXT.strip() not in answer:
        return answer.strip() + DISCLAIMER_TEXT
    return answer

def redact_sensitive_info(answer):
    """(Optional) Redacts sensitive info from the answer if needed. Extend as preferred."""
    # Simple example: Replace confidential words with [REDACTED]
    answer_redacted = answer
    for kw in SENSITIVE_KEYWORDS:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        answer_redacted = pattern.sub("[REDACTED]", answer_redacted)
    return answer_redacted
