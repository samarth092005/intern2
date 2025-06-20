from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from preprocess import load_and_process_data
import joblib

# Load and preprocess
X, y = load_and_process_data()

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)



# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
model = joblib.load("ml/mental_health_model.pkl")

# Save model
import joblib
joblib.dump(model, "ml/mental_health_model.pkl")
