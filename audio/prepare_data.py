import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
from transformers import DistilBertTokenizerFast
import os
import pickle

# 1. Logging current path info
print("📂 Current working dir:", os.getcwd())
print("📁 Files here:", os.listdir())

# 2. Load the dataset (CSV path relative to this script)
df = pd.read_csv("../data/mental_health_text_dataset.csv")

# 3. Encode labels (PTSD=0, Schizophrenia=1, Normal=2)
label_encoder = LabelEncoder()
df['label_enc'] = label_encoder.fit_transform(df['label'])

# 4. Split into train and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(),
    df['label_enc'].tolist(),
    test_size=0.2,
    random_state=42,
    stratify=df['label_enc']
)

# 5. Tokenize using DistilBERT
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# 6. Custom PyTorch Dataset class
class MentalHealthDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    
    def __getitem__(self, idx):
        return {
            'input_ids': torch.tensor(self.encodings['input_ids'][idx]),
            'attention_mask': torch.tensor(self.encodings['attention_mask'][idx]),
            'labels': torch.tensor(self.labels[idx])
        }
    
    def __len__(self):
        return len(self.labels)

# 7. Create datasets
train_dataset = MentalHealthDataset(train_encodings, train_labels)
val_dataset = MentalHealthDataset(val_encodings, val_labels)

# 8. Save datasets and label encoder
os.makedirs("mental_health_dataset", exist_ok=True)
torch.save(train_dataset, "mental_health_dataset/train.pt")
torch.save(val_dataset, "mental_health_dataset/val.pt")

with open("mental_health_dataset/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ All data saved in 'mental_health_dataset' folder.")
