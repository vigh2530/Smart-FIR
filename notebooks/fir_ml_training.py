import pandas as pd
import re
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# ------------------ CONFIG ------------------
DATA_PATH = "D:\Smart_FIR_Legal_AI_Ollama\data\FIR_DATASET.csv"
MODEL_DIR = Path("D:\Smart_FIR_Legal_AI_Ollama\models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "ipc_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
# --------------------------------------------


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()


def main():
    print("📂 Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Auto-detect columns
    text_col = df.columns[0]
    label_col = df.columns[1]

    # ------------------ CRITICAL FIX ------------------
    # Drop rows with missing FIR or IPC section
    df = df[[text_col, label_col]].dropna()

    # Remove empty strings
    df = df[df[text_col].str.strip() != ""]
    df = df[df[label_col].astype(str).str.strip() != ""]
    # --------------------------------------------------

    print(f"✅ Clean dataset size: {len(df)} rows")

    df[text_col] = df[text_col].apply(clean_text)

    print("✂ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
    df[text_col],
    df[label_col],
    test_size=0.2,
    random_state=42
)


    print("🔤 Vectorizing text...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("🤖 Training model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    print("📊 Evaluating...")
    preds = model.predict(X_test_vec)
    acc = accuracy_score(y_test, preds)

    print(f"✅ Model Accuracy: {acc:.4f}")

    print("💾 Saving model & vectorizer...")
    pickle.dump(model, open(MODEL_PATH, "wb"))
    pickle.dump(vectorizer, open(VECTORIZER_PATH, "wb"))

    print("🎉 Training completed successfully!")


if __name__ == "__main__":
    main()
