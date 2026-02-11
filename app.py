import os
import json
import numpy as np
import cv2
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load model
MODEL_PATH = 'model/brain_tumor_resnet_v2.keras'
model = load_model(MODEL_PATH)

# Load class names
with open('model/class_indices.json', 'r') as f:
    indices = json.load(f)
    # Sort by number (0, 1, 2, 3)
    CLASS_NAMES = [k for k, v in sorted(indices.items(), key=lambda item: item[1])]

def prepare_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    upload_path = os.path.join('uploads', file.filename)
    file.save(upload_path)

    # Make prediction
    processed_img = prepare_image(upload_path)
    preds = model.predict(processed_img)
    
    pred_idx = np.argmax(preds[0])
    result = CLASS_NAMES[pred_idx]
    confidence = float(np.max(preds[0]) * 100)

    return jsonify({
        'prediction': result,
        'confidence': f"{confidence:.2f}%"
    })

if __name__ == '__main__':
    # Running on port 5000
    app.run(debug=True, port=5000)
