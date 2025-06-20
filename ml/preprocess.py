import pandas as pd
import pickle

# ----------- FOR TRAINING PURPOSES (OLD LOGIC FOR train_model.py) -----------

def load_and_process_data(path="data/responses.csv"):
    df = pd.read_csv(path)

    # Convert Yes/No to binary
    for col in df.columns[:-1]:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    X = df.drop("label", axis=1)
    y = df["label"]
    return X, y

# ----------- FOR PREDICTION PURPOSES (NEW LOGIC FOR form.py) -----------

# Load the text classifier
with open("ml/text_classifier.pkl", "rb") as f:
    text_clf = pickle.load(f)

# Map Yes/No/Other to numbers
def map_yn(answer):
    answer = answer.lower().strip()
    if "yes" in answer:
        return 2
    elif "no" in answer:
        return 0
    else:
        return 1

# Used by form submission (live user input)
def preprocess_input(input_dict):
    q1_q5 = [map_yn(input_dict[f'q{i}']) for i in range(1, 6)]
    q6_q10_texts = [input_dict[f'q{i}'] for i in range(6, 11)]
    q6_q10_pred = text_clf.predict(q6_q10_texts).tolist()
    return q1_q5 + q6_q10_pred
