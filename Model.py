import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os

# -------------------------------
# Paths
# -------------------------------
MODEL_PATH = "Model_KK.pkl"
IMAGE_PATH = "Model_KK"   # change this to your actual image filename

# -------------------------------
# Load the trained model
# -------------------------------
if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found: {MODEL_PATH}")
    st.stop()

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="L&T Hardness Predictor", layout="centered")

st.title("🔧 L&T Hardness Predictor")
st.write("Enter the material processing parameters below to predict the hardness.")

# Display image if available
if os.path.exists(IMAGE_PATH):
    img = Image.open(IMAGE_PATH)
    st.image(img, caption="Heat Treatment Illustration", use_column_width=True)

st.subheader("Input Parameters")

carbon = st.number_input("Carbon Content (%)", min_value=0.0, max_value=2.0, step=0.01)

austen_temp = st.number_input("Austenitizing Temperature (°C)", min_value=600, max_value=1200, step=10)

quench_medium = st.selectbox(
    "Quenching Medium",
    ["Water", "Oil", "Polymer", "Air"]
)

temper_temp = st.number_input("Tempering Temperature (°C)", min_value=100, max_value=700, step=10)

temper_time = st.number_input("Tempering Time (minutes)", min_value=1, max_value=300, step=1)

# Convert categorical field
quench_dict = {"Water": 0, "Oil": 1, "Polymer": 2, "Air": 3}
quench_value = quench_dict[quench_medium]

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Hardness"):
    try:
        input_data = np.array([[carbon, austen_temp, quench_value, temper_temp, temper_time]])
        prediction = model.predict(input_data)[0]
        st.success(f"### 🔨 Predicted Hardness: **{prediction:.2f} HV**")
    except Exception as e:
        st.error("Error during prediction. Please check inputs or model.")
        st.write(e)

st.markdown("---")
st.caption("Developed by Krish — L&T Hardness Prediction System")
