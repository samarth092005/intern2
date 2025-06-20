from ml.preprocess import preprocess_input
import joblib
import pandas as pd
import os

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "mental_health_model.pkl")
model = joblib.load(model_path)

def predict_disorder(responses):
    # Step 1: Preprocess inputs using your updated function
    processed_input = preprocess_input(responses)

    # Step 2: Build DataFrame with correct column names
    columns = [f"q{i}" for i in range(1, 11)]
    df_input = pd.DataFrame([processed_input], columns=columns)

    # Debug: Show what model is receiving
    print("Model Input:")
    print(df_input)

    # Step 3: Predict
    prediction = model.predict(df_input)[0]
    proba = model.predict_proba(df_input)[0]

    # Step 4: Severity Score (based on number of '1's)
    severity = sum(processed_input)

    return prediction, severity
