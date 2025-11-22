import streamlit as st
import numpy as np
import pickle
from PIL import Image

# -------------------------------
# Load the trained model
# -------------------------------
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="L&T Hardness Predictor", layout="centered")

st.title("🔧 L&T Hardness Predictor")
st.write("Enter the material processing parameters below to predict the hardness.")

# -------------------------------
# User Inputs
# -------------------------------
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
# Image Upload (Optional)
# -------------------------------
st.subheader("Upload Microstructure Image (Optional)")
uploaded_image = st.file_uploader("Upload PNG/JPG microstructure image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Microstructure", use_column_width=True)

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
