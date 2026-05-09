import json
import pickle
import os

model = None
vectorizer = None

# =========================
# Initialize model
# =========================

def init():
    global model, vectorizer

    model_dir = os.getenv("AZUREML_MODEL_DIR", ".")

    model_path = os.path.join(model_dir, "deployment_files", "model.pkl")
    vectorizer_path = os.path.join(model_dir, "deployment_files", "vectorizer.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

# =========================
# Prediction Function
# =========================

def run(data):

    try:
        data = json.loads(data)

        text = data["text"]

        vect = vectorizer.transform([text])

        prediction = model.predict(vect)[0]

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