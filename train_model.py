import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import os

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

# ✅ Collapse rare localities to reduce one-hot explosion
locality_counts = df['Locality'].value_counts()
df['Locality'] = df['Locality'].apply(
    lambda x: x if locality_counts[x] > 50 else "Other"
)

# Features and target
X = df[[
    "City","Locality", "Public_Transport_Accessibility", "Parking_Space", "Security",
    "Facing", "Owner_Type", "Availability_Status",
    "BHK", "Size_in_SqFt",
    "Playground", "Gym", "Garden", "Pool", "Clubhouse"
]]
y = df["Price_per_SqFt"]

# Define categorical and numeric features
categorical = ["City", "Locality", "Public_Transport_Accessibility", "Parking_Space",
               "Security", "Facing", "Owner_Type", "Availability_Status"]
numeric = ["BHK", "Size_in_SqFt", "Playground", "Gym", "Garden", "Pool", "Clubhouse"]

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ]
)

# Build pipeline with lighter RandomForest
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=20,       # fewer trees → smaller file
        max_depth=10,          # limit depth
        random_state=42,
        n_jobs=-1
    ))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("✅ RandomForest model trained successfully with City + Locality grouping!")
print(f"R² Score: {r2:.3f}")
print(f"Mean Absolute Error: {mae:.2f}")

# Ensure models folder exists
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/price_prediction_model.joblib")
print("💾 Model saved to models/price_prediction_model.joblib")
