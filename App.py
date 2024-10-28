from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Loading the pre-trained model
model = joblib.load('heart_disease_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from the request
        data = request.json
        
        # Validate input data
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing data"}), 400
        
        # Convert inputs to the correct type and check ranges
        features = []
        try:
            features.append(int(data['age']))
            features.append(int(data['sex']))
            features.append(int(data['cp']))
            features.append(int(data['trestbps']))
            features.append(int(data['chol']))
            features.append(int(data['fbs']))
            features.append(int(data['restecg']))
            features.append(int(data['thalach']))
            features.append(int(data['exang']))
            features.append(float(data['oldpeak']))
            features.append(int(data['slope']))
            features.append(int(data['ca']))
            features.append(int(data['thal']))
        except ValueError:
            return jsonify({"error": "Invalid input data types"}), 400

        # Reshape features for prediction
        features = np.array(features).reshape(1, -1)

        # Predict and return result
        prediction = model.predict_proba(features)[0][1]  # Assuming a probability output
        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
