import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle

# Step 1: Create synthetic dataset
np.random.seed(42)

num_samples = 500

attendance = np.random.randint(30, 100, num_samples)
assignments = np.random.randint(30, 100, num_samples)
marks = np.random.randint(30, 100, num_samples)
study_hours = np.random.randint(1, 30, num_samples)
participation = np.random.randint(1, 10, num_samples)

# Logic to determine dropout (simple rule-based labeling)
dropout = (
    (attendance < 50) |
    (marks < 50) |
    (assignments < 50)
).astype(int)

data = pd.DataFrame({
    "attendance": attendance,
    "assignments": assignments,
    "marks": marks,
    "study_hours": study_hours,
    "participation": participation,
    "dropout": dropout
})

# Step 2: Split data
X = data.drop("dropout", axis=1)
y = data["dropout"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 3: Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 4: Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("Model Accuracy:", accuracy)
print("Confusion Matrix:\n", cm)

# Step 5: Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as model.pkl")
