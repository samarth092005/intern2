import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Load tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)
model.load_state_dict(torch.load("audio/mental_health_dataset/trained_model.pt", map_location=torch.device("cpu")))

model.eval()

# Define class labels
label_mapping = {
    0: "PTSD",
    1: "Schizophrenia",
    2: "Depression",
    3: "Healthy"
}

# ✅ Prediction function returns both disorder and score
def predict_disorder(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs).item()
        confidence = round(probs[0][predicted_class].item() * 100, 2)  # percentage
        return label_mapping[predicted_class], confidence
