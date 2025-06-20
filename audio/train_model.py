import torch
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
from prepare_data import MentalHealthDataset  # Custom dataset class
import os

# ✅ Show current working directory (for debugging)
print("📂 Current working dir:", os.getcwd())

# ✅ Load encoded datasets saved earlier
train_dataset = torch.load("mental_health_dataset/train.pt", weights_only=False)
val_dataset = torch.load("mental_health_dataset/val.pt", weights_only=False)

# ✅ Load DistilBERT base model with 3 output labels
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)

# ✅ Define training configuration
training_args = TrainingArguments(
    output_dir="./distilbert_output",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    weight_decay=0.01,
    logging_dir="./logs",
    load_best_model_at_end=True,
)

# ✅ Create Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# ✅ Start fine-tuning
trainer.train()

# ✅ Save full model (optional, in case you want to upload to Huggingface later)
model.save_pretrained("saved_model")
print("✅ Full model saved to: saved_model/")

# ✅ Save model state_dict to expected path for Flask app
torch.save(model.state_dict(), "mental_health_dataset/trained_model.pt")
print("✅ Model saved to: mental_health_dataset/trained_model.pt")

