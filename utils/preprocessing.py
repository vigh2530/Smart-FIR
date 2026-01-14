import re

HINGLISH_MAP = {
    "chor": "thief",
    "theif": "thief",
    "chura": "stolen",
    "stole": "stolen",
    "loot": "robbery",
    "maar": "assault"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

def normalize_hinglish(text):
    words = text.split()
    normalized = [HINGLISH_MAP.get(w, w) for w in words]
    return " ".join(normalized)

def preprocess_fir(text):
    text = normalize_hinglish(text)
    text = clean_text(text)
    return text
