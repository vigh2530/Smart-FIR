def check_fir_quality(text):
    warnings = []
    score = 100

    words = text.split()

    if len(words) < 8:
        warnings.append("FIR description too short.")
        score -= 25

    if not any(w in text for w in ["am", "pm", "morning", "evening", "night"]):
        warnings.append("Time of incident missing.")
        score -= 15

    if not any(w in text for w in ["road", "house", "market", "bus", "station"]):
        warnings.append("Location details missing.")
        score -= 15

    if not any(w in text for w in ["stolen", "assault", "hit", "attack", "rob"]):
        warnings.append("Action details unclear.")
        score -= 15

    return {
        "quality_score": max(score, 0),
        "warnings": warnings
    }
