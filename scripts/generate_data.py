import pandas as pd
import random

def generate_sample(label):
    sample = []
    for i in range(10):
        if label == "PTSD":
            sample.append("Yes" if i in [0, 2, 4, 8] else random.choice(["Yes", "No"]))
        elif label == "Schizophrenia":
            sample.append("Yes" if i in [1, 3, 5, 7] else random.choice(["Yes", "No"]))
        else:  # Healthy
            sample.append("No")
    return sample + [label]

data = []
for _ in range(50):
    label = random.choice(["PTSD", "Schizophrenia", "Healthy"])
    data.append(generate_sample(label))

df = pd.DataFrame(data, columns=[f"q{i+1}" for i in range(10)] + ["label"])
df.to_csv("data/responses.csv", index=False)

print("✅ Symptom-based data saved to data/responses.csv")
