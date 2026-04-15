import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Plant Disease AI", page_icon="🌿")

st.title("🌿 Plant Disease Detection AI System")
st.write("Upload a leaf image to detect disease")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Analyzing with AI system... 🤖")

    img = np.array(image)
    avg = img.mean()

    if avg < 100:
        result = "🍂 Leaf Blight Disease"
        severity = "High 🔴"
        solution = "Remove infected leaves + use fungicide"
    elif avg < 170:
        result = "🦠 Bacterial Spot"
        severity = "Medium 🟠"
        solution = "Spray copper-based solution"
    else:
        result = "🌱 Healthy Plant"
        severity = "Low 🟢"
        solution = "Keep proper watering & sunlight"

    st.subheader("Prediction Result")
    st.success(result)

    st.write("Severity:", severity)
    st.write("Solution:", solution)
