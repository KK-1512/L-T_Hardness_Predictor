import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image

# ---------------------------------------------------------
#                LOAD MODEL
# ---------------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("steel_hardness_model.pkl")  # <-- Replace name if different

model = load_model()

# ---------------------------------------------------------
#                UI SETUP
# ---------------------------------------------------------

st.set_page_config(page_title="Steel Hardness Predictor", layout="wide")

st.title("🔧 Steel Hardness Prediction Using Machine Learning")
st.write("""
This tool predicts the **Hardness (HRC)** of steel after heat treatment  
based on chemical composition and processing parameters.
""")

# ---------------------------------------------------------
#                IMAGE UPLOAD (OPTIONAL)
# ---------------------------------------------------------

st.subheader("📷 Upload an Image (logo, diagram, specimen photo)")

uploaded_img = st.file_uploader("Upload JPG/PNG image", type=["jpg", "jpeg", "png"])

if uploaded_img is not None:
    img = Image.open(uploaded_img)
    st.image(img, caption="Uploaded Image", width=300)

st.markdown("---")

# ---------------------------------------------------------
#                INPUT FORM
# ---------------------------------------------------------

st.subheader("Enter Input Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    C = st.number_input("Carbon (C %):", 0.00, 1.50, 0.45)
    Mn = st.number_input("Manganese (Mn %):", 0.00, 2.00, 0.75)
    Si = st.number_input("Silicon (Si %):", 0.00, 2.00, 0.25)

with col2:
    Cr = st.number_input("Chromium (Cr %):", 0.00, 3.00, 0.50)
    Ni = st.number_input("Nickel (Ni %):", 0.00, 3.00, 0.40)
    Mo = st.number_input("Molybdenum (Mo %):", 0.00, 1.50, 0.20)

with col3:
    austen_temp = st.number_input("Austenitizing Temperature (°C):", 700, 1200, 850)
    hold_time = st.number_input("Hold Time (min):", 1, 300, 60)
    quench_medium = st.selectbox("Quench Medium:", ["Water", "Oil", "Polymer"])

tempering_temp = st.number_input("Tempering Temperature (°C):", 100, 700, 300)
tempering_time = st.number_input("Tempering Time (min):", 1, 500, 120)

# Composition source (for dataset consistency)
source = st.selectbox("Data Source Category:", 
                      ["MDPI", "Mendeley", "S45C study", "ST37 study", "Synthetic"])

# ---------------------------------------------------------
#                PREDICTION
# ---------------------------------------------------------

if st.button("Predict Hardness (HRC)"):
    # Build dataframe to send to model
    input_data = pd.DataFrame([{
        "C": C,
        "Mn": Mn,
        "Si": Si,
        "Cr": Cr,
        "Ni": Ni,
        "Mo": Mo,
        "austenitizing_temp": austen_temp,
        "hold_time": hold_time,
        "quench_medium": quench_medium,
        "tempering_temp": tempering_temp,
        "tempering_time": tempering_time,
        "composition_source": source
    }])

    # Predict
    hardness_pred = model.predict(input_data)[0]

    st.success(f"### 🔩 Predicted Hardness: **{hardness_pred:.2f} HRC**")

# ---------------------------------------------------------
#                FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.write("Developed by Krish — Metallurgy GET Interview Project (L&T)")
