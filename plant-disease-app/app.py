import streamlit as st
from PIL import Image
import numpy as np

st.title("🌿 Plant Disease Detector")

uploaded_file = st.file_uploader("Upload plant leaf image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    img = np.array(image)
    avg = img.mean()

    if avg < 100:
        result = "🍂 Leaf Blight Disease"
        severity = "High 🔴"
    elif avg < 170:
        result = "🦠 Bacterial Spot"
        severity = "Medium 🟠"
    else:
        result = "🌱 Healthy Plant"
        severity = "Low 🟢"

    st.subheader("Prediction")
    st.success(result)
    st.write("Severity:", severity)
    
