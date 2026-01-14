import streamlit as st
import pickle

from utils.preprocessing import preprocess_fir
from utils.fir_quality import check_fir_quality
from utils.explainability import get_top_keywords

from ollama.ollama_client import call_ollama
from ollama.prompts import (
    ipc_explanation_prompt,
    punishment_prompt
)

# ---------------- CONFIG ----------------
CONFIDENCE_THRESHOLD = 0.30
# ----------------------------------------


# Load ML artifacts
model = pickle.load(open("models/ipc_model.pkl", "rb"))
vectorizer = pickle.load(open("models/tfidf_vectorizer.pkl", "rb"))

st.set_page_config(page_title="Smart FIR Legal AI", layout="wide")
st.title("🚨 Smart FIR Legal Intelligence System")

fir_input = st.text_area("Enter FIR Description")

if st.button("Analyze FIR") and fir_input.strip():
    with st.spinner("Analyzing FIR..."):

        # ---------- PREPROCESS ----------
        processed = preprocess_fir(fir_input)

        # ---------- ML PREDICTION ----------
        vec = vectorizer.transform([processed])
        probs = model.predict_proba(vec)[0]
        classes = model.classes_

        top3 = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
        primary_ipc, primary_conf = top3[0]

        use_llm_only = primary_conf < CONFIDENCE_THRESHOLD

        # ---------- FIR QUALITY ----------
        quality = check_fir_quality(processed)

        # ---------- KEYWORDS ----------
        keywords = get_top_keywords(model, vectorizer, processed)

        # ---------- IPC DETERMINATION ----------
        if use_llm_only:
            llm_ipc = call_ollama(
                f"""
You are an expert in Indian Penal Code.

Based ONLY on the FIR below, identify the most applicable IPC section(s).
Return IPC number and name.

FIR:
{processed}

Respond concisely.
"""
            )
            final_ipc = llm_ipc
        else:
            final_ipc = primary_ipc

        # ---------- SEVERITY (FIR-BASED ONLY) ----------
        severity = call_ollama(
            f"""
Classify the crime severity as Low, Medium, or High
based ONLY on the FIR description.

FIR:
{processed}

Give severity and short reason.
"""
        )

        # ---------- LEGAL EXPLANATION ----------
        explanation = call_ollama(
            f"""
Explain in simple legal terms why the following IPC section(s)
apply to the FIR.

FIR:
{processed}

IPC:
{final_ipc}
"""
        )

        # ---------- PUNISHMENT ----------
        punishment = call_ollama(
            punishment_prompt(final_ipc)
        )

    # ================= UI OUTPUT =================

    st.subheader("🔍 IPC Prediction")

    if use_llm_only:
        st.warning(
            "ML confidence is low. Using LLM-based legal reasoning "
            "to ensure correctness."
        )
        st.write(final_ipc)
    else:
        for sec, prob in top3:
            st.write(f"IPC {sec} — {round(prob*100,2)}%")

    st.subheader("⚠ FIR Quality")
    st.write("Score:", quality["quality_score"])
    for w in quality["warnings"]:
        st.warning(w)

    st.subheader("🧠 Explainable Keywords")
    st.write(keywords)

    st.subheader("📊 Severity Analysis")
    st.write(severity)

    st.subheader("⚖ Legal Explanation")
    st.write(explanation)

    st.subheader("📜 Punishment")
    st.write(punishment)
