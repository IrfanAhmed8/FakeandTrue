from flask import Flask, request, jsonify
import pickle

# =========================
# Load model and vectorizer
# =========================

model = pickle.load(open("deployment_files/model.pkl", "rb"))
vectorizer = pickle.load(open("deployment_files/vectorizer.pkl", "rb"))

# =========================
# Create Flask app
# =========================

app = Flask(__name__)

# =========================
# Home route
# =========================

@app.route('/')
def home():
    return "Fake News Detector API is running!"

# =========================
# Prediction route
# =========================

@app.route('/predict', methods=['POST'])
def predict():

    try:
        data = request.get_json()

        text = data['text']

        # Transform text
        vect = vectorizer.transform([text])

        # Predict
        prediction = model.predict(vect)[0]

        # Confidence score
        confidence = model.predict_proba(vect)[0].max()

        result = "Real" if prediction == 1 else "Fake"

        return jsonify({
            "result": result,
            "confidence": round(float(confidence) * 100, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

# =========================
# Run app
# =========================

if __name__ == '__main__':
    app.run(debug=True)