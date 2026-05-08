import pickle
import json
import os

model = None
vectorizer = None

# =========================
# Initialize model
# =========================

def init():
    global model, vectorizer

    model_dir = os.getenv("AZUREML_MODEL_DIR", ".")

    model_path = os.path.join(model_dir, "model.pkl")
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")

    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Load vectorizer
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

# =========================
# Prediction function
# =========================

def run(data):
    try:
        data = json.loads(data)

        text = data["text"]

        # Transform text
        vect = vectorizer.transform([text])

        # Predict
        prediction = model.predict(vect)[0]

        # Confidence score
        confidence = model.predict_proba(vect)[0].max()

        result = "Real" if prediction == 1 else "Fake"

        return {
            "result": result,
            "confidence": round(float(confidence) * 100, 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }