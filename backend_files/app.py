import os
import pandas as pd
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'superkart_model.joblib')
model = joblib.load(model_path)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        # Convert inputs into the DataFrame format required by the pipeline
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)
        return jsonify({"prediction": float(prediction[0])}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Load CSV into DataFrame
        input_df = pd.read_csv(file)
        predictions = model.predict(input_df)
        
        # Map index to prediction output
        results = {int(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
