import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# =========================
# Load datasets
# =========================

fake = pd.read_csv("data/Fake.csv")
real = pd.read_csv("data/True.csv")

# Add labels
fake["label"] = 0
real["label"] = 1

# Combine datasets
data = pd.concat([fake, real])

# Shuffle data properly
data = data.sample(frac=1, random_state=42)

# =========================
# Features and labels
# =========================

X = data["text"]
y = data["label"]

# =========================
# Text Vectorization
# =========================

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_df=0.7
)

X = vectorizer.fit_transform(X)

# =========================
# Train/Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# Train Model
# =========================

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# =========================
# Evaluate Model
# =========================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(accuracy)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# =========================
# Save Model
# =========================

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\nModel and vectorizer saved successfully!")