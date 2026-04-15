from flask import Flask, render_template, request
from PIL import Image
import os
from transformers import pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load AI model
print("Loading AI model...")
classifier = pipeline("image-classification", model="microsoft/resnet-50")
print("Model loaded!")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']

    if file.filename == '':
        return "No file selected"

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    image = Image.open(path)

    result = classifier(image)[0]

    label = result['label'].lower()
    confidence = result['score']

    # Smart override
    if "pot" in label or "plant" in label:
        label = "Possible Plant Disease Detected"

    # Severity logic
    if "possible plant disease detected" in label:
        if confidence < 0.60:
            severity = "Low 🟢"
        elif confidence < 0.80:
            severity = "Medium 🟡"
        else:
            severity = "High 🔴"
    else:
        severity = "No Disease ✅"

    # Cure logic
    if "possible plant disease detected" in label:
        cure = "Possible infection detected. Use neem oil or fungicide spray and remove affected leaves."
    else:
        cure = "Plant looks healthy. Maintain proper watering, sunlight, and soil nutrients."

    # RESULT PAGE (FIXED UI)
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Plant Disease Result</title>
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial;
            background: linear-gradient(to right, #56ab2f, #a8e063);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}

        .card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            width: 380px;
            max-width: 90%;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        h2 {{
            margin-bottom: 15px;
        }}

        .value {{
            margin-bottom: 12px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}

        p {{
            font-size: 14px;
            word-break: break-word;
        }}

        .label {{
            font-weight: bold;
            color: #333;
        }}

        .btn {{
            margin-top: 15px;
            padding: 10px 18px;
            background: black;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            display: inline-block;
        }}

        .btn:hover {{
            background: #333;
        }}
    </style>
</head>

<body>

<div class="card">

    <h2>🌿 Detection Result</h2>

    <div class="value">
        <span class="label">Prediction:</span><br>
        <p>{label}</p>
    </div>

    <div class="value">
        <span class="label">Confidence:</span><br>
        <p>{confidence:.2f}</p>
    </div>

    <div class="value">
        <span class="label">Severity Level:</span><br>
        <p><b>{severity}</b></p>
    </div>

    <div class="value">
        <span class="label">Solution:</span><br>
        <p>{cure}</p>
    </div>

    <a href="/" class="btn">🔙 Try Another</a>

</div>

</body>
</html>
"""


if __name__ == "__main__":
    print("Flask running...")
    app.run(debug=True)