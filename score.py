import pickle
import json
import os

def init():
    global model, vectorizer

    model_dir = os.getenv("AZUREML_MODEL_DIR")

    # Try multiple possible paths (robust fix)
    possible_paths = [
        os.path.join(model_dir, "model.pkl"),
        os.path.join(model_dir, "vectorizer.pkl"),
        os.path.join(model_dir, "fake-news-model", "model.pkl"),
        os.path.join(model_dir, "fake-news-model", "vectorizer.pkl"),
    ]

    # Find correct paths
    model_path = None
    vectorizer_path = None

    for path in possible_paths:
        if "model.pkl" in path and os.path.exists(path):
            model_path = path
        if "vectorizer.pkl" in path and os.path.exists(path):
            vectorizer_path = path

    if model_path is None or vectorizer_path is None:
        raise Exception("Model or vectorizer file not found")

    model = pickle.load(open(model_path, "rb"))
    vectorizer = pickle.load(open(vectorizer_path, "rb"))

def run(data):
    try:
        data = json.loads(data)
        text = data["text"]

        vect = vectorizer.transform([text])
        prediction = model.predict(vect)[0]

        return {"result": "Real" if prediction == 1 else "Fake"}
    
    except Exception as e:
        return {"error": str(e)}