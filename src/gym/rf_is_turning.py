import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # Import classifier
from sklearn.metrics import classification_report  # Import classification metrics
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import GridSearchCV
import numpy as np
import time
plt.switch_backend('TkAgg')

# Initialize grid search params
param_grid = {
    "n_estimators": [80, 90, 100, 150],
    "max_depth": [None, 2, 3, 4, 5, 10],
    "min_samples_split": [2, 3, 5, 7],
    "min_samples_leaf": [1, 2, 3, 4, 5],
    "bootstrap": [True, False],
    "criterion": ['gini', 'entropy'] # Criteria for information gain.
}

joined_features = pd.DataFrame(
    columns=["magneticFieldZ", "accelerationY", "angularVelocityZ", "heading"]
)
joined_targets = pd.DataFrame(columns=["steering"])

# Reading and processing loop – remains the same except for turn into binary classification logic
for i in range(1, 7):  # 1 to 6 inclusive
    # Setup paths to read from
    steering_file = f"../datasets/full/car.{i}.steering.txt"
    magneticZ_file = f"../datasets/full/car.{i}.mag.z.txt"
    accelerationY_file = f"../datasets/full/car.{i}.acceleration.y.txt"
    velocityZ_file = f"../datasets/full/car.{i}.velocity.z.txt"
    heading_file = f"../datasets/full/car.{i}.heading.txt"

    # Read datasets into dataframes
    steering = pd.read_csv(steering_file, names=["steering"])
    magneticZ = pd.read_csv(magneticZ_file, names=["magneticFieldZ"])
    accelerationY = pd.read_csv(accelerationY_file, names=["accelerationY"])
    velocityZ = pd.read_csv(velocityZ_file, names=["angularVelocityZ"])
    heading = pd.read_csv(heading_file, names=["heading"])
    
    # Turn into binary classification
    steering['steering'] = (steering['steering'] != 0).astype(int)

    # Concatenate dataframes into single feature set
    features = pd.concat([magneticZ, accelerationY, velocityZ, heading], axis=1)

    # Concatenate dataframes with previous dataframes
    joined_features = pd.concat([joined_features, features], ignore_index=True)
    joined_targets = pd.concat([joined_targets, steering], ignore_index=True)

X = joined_features
y = joined_targets['steering']  # We use the processed binary target directly

# Split X and y into training and test datasets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features (input variables)
X_scaler = MinMaxScaler()
X_train_scaled = X_scaler.fit_transform(X_train)
X_test_scaled = X_scaler.transform(X_test)
print("Unique values in y_train:", np.unique(y_train))
print("Data type of y_train:", y_train.dtype)

# Ensure y_train is integer (as needed for classification in Scikit-learn)
if y_train.dtype != np.int64:
    y_train = y_train.astype('int')
    y_test = y_test.astype('int')
print(y_train.head())
print(y_test.head())
# Initialize the RF classifier with a random state for reproducibility
model = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,
    n_jobs=-1,
    verbose=2,
    scoring="accuracy",
)

# Train model using Grid Search with scaled inputs and targets
grid_search.fit(X_train_scaled, y_train)

best_model = grid_search.best_estimator_
predictions = best_model.predict(X_test_scaled)
print("Best Parameters:", grid_search.best_params_)

# Evaluation using classification metrics
print(classification_report(y_test, predictions))

# Plotting predictions - here, we plot the count of each class predicted
plt.figure(figsize=(8, 4))
plt.hist(predictions, bins=2, alpha=0.7, color='red', label='Predicted', align='left')
plt.hist(y_test, bins=2, alpha=0.7, color='black', label='Actual', align='right')
plt.title("Comparison of Prediction and Actual")
plt.xlabel("Class")
plt.ylabel("Frequency")
plt.legend(loc="upper right")
plt.show()

# Save model and scalers
model_id = str(time.time())
joblib.dump(best_model, model_id + "-model.joblib")
joblib.dump(X_scaler, model_id + "-feature-scaler.joblib")
