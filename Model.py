import streamlit as st
import pandas as pd
from PIL import Image
from Model import HardnessPredictor

# ---------------------------------------------------------
# Load Model
# ---------------------------------------------------------
predictor = HardnessPredictor("steel_hardness_predictor.pkl")

st.set_page_config(page_title="Steel Hardness Predictor", layout="wide")

st.title("🔧 Steel Hardness Prediction Using Machine Learning")
st.write("""
This tool predicts the **Hardness (HRC)** of steel after heat treatment  
based on chemical composition and processing parameters.
""")

# ---------------------------------------------------------
# Image Upload Section
# ---------------------------------------------------------

st.subheader("📷 Upload an Image (Optional — logo or heat-treatment diagram)")
img_file = st.file_uploader("Upload JPG/PNG image", type=["jpg", "jpeg", "png"])

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Uploaded Image", width=350)

st.divider()

# ---------------------------------------------------------
# Input Form
# ---------------------------------------------------------

st.subheader("Enter Heat Treatment & Composition Parameters:")

col1, col2, col3 = st.columns(3)

with col1:
    C = st.number_input("Carbon (wt%)", 0.00, 1.50, 0.45)
    Mn = st.number_input("Manganese (wt%)", 0.00, 2.00, 0.75)
    Si = st.number_input("Silicon (wt%)", 0.00, 2.00, 0.20)

with col2:
    Cr = st.number_input("Chromium (wt%)", 0.00, 3.00, 0.70)
    Ni = st.number_input("Nickel (wt%)", 0.00, 3.00, 0.20)
    Mo = st.number_input("Molybdenum (wt%)", 0.00, 1.50, 0.15)

with col3:
    aust_temp = st.number_input("Austenitize Temperature (°C)", 650, 1200, 900)
    aust_time = st.number_input("Hold Time (min)", 1, 300, 45)
    quench_medium = st.selectbox("Quench Medium", ["Water", "Oil", "Polymer"])

temper_temp = st.number_input("Tempering
