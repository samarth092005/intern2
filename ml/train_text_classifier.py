import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training data
data = {
    "text": [
        "Yes", "No", "Sometimes", "I feel anxious a lot",
        "I am totally fine", "Not really", "Absolutely", 
        "I don’t know", "Maybe", "I often feel low"
    ],
    "label": [2, 0, 1, 2, 0, 0, 2, 1, 1, 2]
}

df = pd.DataFrame(data)

# Train text classifier
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(df["text"], df["label"])

# Save model
with open("ml/text_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Trained and saved text_classifier.pkl")
