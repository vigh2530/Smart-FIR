import pandas as pd
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
print("📂 Loading dataset...")
df = pd.read_csv("data/FIR_DATASET.csv")

# Rename columns if needed
df.columns = [c.strip() for c in df.columns]

# Extract IPC section numbers from URL
df['IPC'] = df['URL'].str.extract(r'section-(\d+)')

# Filter to IPC sections with at least 3 samples (enables CV splits)
ipc_counts = df['IPC'].value_counts()
valid_ipcs = ipc_counts[ipc_counts >= 3].index
df = df[df['IPC'].isin(valid_ipcs)].reset_index(drop=True)

print(f"✅ Filtered dataset: {len(valid_ipcs)} IPC sections, {len(df)} total samples")
print(f"   Sample distribution - Min: {ipc_counts[ipc_counts >= 3].min()}, Max: {ipc_counts[ipc_counts >= 3].max()}")

# Use Description as text and IPC as label
TEXT_COL = 'Description'
LABEL_COL = 'IPC'

# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

df[TEXT_COL] = df[TEXT_COL].astype(str).apply(clean_text)

# Train-test split with stratification
print("✂ Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    df[TEXT_COL],
    df[LABEL_COL],
    test_size=0.2,
    random_state=42,
    stratify=df[LABEL_COL]
)

# TF-IDF
print("🔤 Vectorizing text...")
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=2000,
    min_df=2,
    max_df=0.8
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print(f"   Features created: {X_train_vec.shape[1]}")

# Model with class weights to handle imbalance
print("🤖 Training model...")
model = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    solver='lbfgs',
    random_state=42
)
model.fit(X_train_vec, y_train)

# Evaluation
print("📊 Evaluating...")
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy:.4f}")
print(f"📈 Accuracy %: {accuracy*100:.2f}%")
print(f"\n📋 Classification Report (first 50 lines):")
report = classification_report(y_test, y_pred, zero_division=0)
print('\n'.join(report.split('\n')[:50]))

# Save model & vectorizer
print("\n💾 Saving model & vectorizer...")
pickle.dump(model, open("models/ipc_model.pkl", "wb"))
pickle.dump(vectorizer, open("models/tfidf_vectorizer.pkl", "wb"))

print("🎉 Training completed successfully!")
