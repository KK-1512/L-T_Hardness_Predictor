import os
import joblib
import numpy as np
import pandas as pd

class HardnessPredictor:
    """
    Class to load the trained model and make hardness predictions for steel
    after heat treatment based on composition & process parameters.
    """

    def __init__(self, model_path: str = "steel_hardness_predictor.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at path: {model_path}")
        self.model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")

        # List of expected features in the correct order
        self.expected_features = [
            "C_wt%", "Mn_wt%", "Si_wt%", "Cr_wt%", "Ni_wt%", "Mo_wt%",
            "Austenitize_Temp_C", "Hold_Time_min",
            "Quench_Medium",  # categorical
            "Temper_Temp_C", "Temper_Time_min",
            "Cooling_Rate_Proxy"
        ]

    def prepare_input(self, input_dict: dict) -> pd.DataFrame:
        """
        Validate and prepare a single input dict and return a pandas DataFrame
        ready for model.predict().
        """
        df = pd.DataFrame([input_dict])

        missing = [f for f in self.expected_features if f not in df.columns]
        if missing:
            raise ValueError(f"Missing features in input: {missing}")

        # Reorder columns
        df = df[self.expected_features]

        return df

    def predict(self, input_dict: dict) -> float:
        """
        Given a dictionary of input features, return predicted hardness (HRC).
        """
        df = self.prepare_input(input_dict)

        try:
            pred = self.model.predict(df)[0]
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")

        return float(pred)

if __name__ == "__main__":
    # Example usage
    predictor = HardnessPredictor(model_path="steel_hardness_predictor.pkl")

    sample_input = {
        "C_wt%": 0.42,
        "Mn_wt%": 0.75,
        "Si_wt%": 0.18,
        "Cr_wt%": 0.50,
        "Ni_wt%": 0.20,
        "Mo_wt%": 0.10,
        "Austenitize_Temp_C": 900,
        "Hold_Time_min": 40,
        "Quench_Medium": "Water",
        "Temper_Temp_C": 500,
        "Temper_Time_min": 60,
        "Cooling_Rate_Proxy": 3
    }

    predicted_hardness = predictor.predict(sample_input)
    print(f"Predicted Hardness (HRC): {predicted_hardness:.2f}")

# ---------------------------------------------------------
#                FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.write("Developed by Krish — Metallurgy GET Interview Project (L&T)")
