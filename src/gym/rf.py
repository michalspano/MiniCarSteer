# LLM: 7.txt, 8.txt, 9.txt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from joblib import dump
from sklearn.model_selection import GridSearchCV
import numpy as np
from time import time
plt.switch_backend("TkAgg")
# Initialize grid search params
param_grid = {
    "n_estimators": [
        500,
    ],
    "max_depth": [None, 2, 3, 4,],
    "min_samples_split": [2, 3,],
    "min_samples_leaf": [1, 2, 3],
    "bootstrap": [True],
}


# Initialize empty DataFrames for features and target
joined_features = pd.DataFrame(
    columns=[
        "angularVelocityX",
        "angularVelocityY",
        "angularVelocityZ",
        "magneticFieldX",
        "magneticFieldY",
        "magneticFieldZ",
        "accelerationX",
        "accelerationY",
        "accelerationZ",
        "heading",
        "pedal",
        "voltage",
        "distance",
    ]
)
joined_targets = pd.DataFrame(columns=["groundSteeringRequest"])

# Loop through the files for 6 cars. LLM: 6.txt
for i in range(1, 6):  # 1 to 6 inclusive
    # Setup the paths to read from
    carData = f"../datasets/car.{i}.txt"
    # Read datasets into dataframes
    car = pd.read_csv(
        carData,
        sep=",",
        header=0,
        names=[
            "groundSteeringRequest",
            "angularVelocityX",
            "angularVelocityY",
            "angularVelocityZ",
            "magneticFieldX",
            "magneticFieldY",
            "magneticFieldZ",
            "accelerationX",
            "accelerationY",
            "accelerationZ",
            "heading",
            "pedal",
            "voltage",
            "distance",
        ],
    )
    # Concatenate dataframes into single feature set
    features = car[
        [
            "angularVelocityX",
            "angularVelocityY",
            "angularVelocityZ",
            "magneticFieldX",
            "magneticFieldY",
            "magneticFieldZ",
            "accelerationX",
            "accelerationY",
            "accelerationZ",
            "heading",
            "pedal",
            "voltage",
            "distance",
        ]
    ]
    # Concatenate dataframes with previous dataframes
    joined_features = pd.concat([joined_features, features], axis=0, ignore_index=True)
    target = car[["groundSteeringRequest"]].reset_index(
        drop=True
    )  # Ensure it's a DataFrame
    joined_targets = pd.concat([joined_targets, target], axis=0, ignore_index=True)

X = joined_features
y = joined_targets.values.reshape(
    -1, 1
)  # We need to reshape this into a 2D array since train_test_split expects 2D array

# Split X input and target y into their respective datasets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.01, random_state=42
)

# Initialize the RF model with a random state for reproducibility
model = RandomForestRegressor(random_state=42)


grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,
    n_jobs=-1,
    verbose=2,
    scoring="neg_mean_squared_error",
)

# Train model with Grid Search using inputs and targets
grid_search.fit(X_train, y_train.ravel())


best_model = grid_search.best_estimator_
predictions = best_model.predict(X_test)
print("Best Parameters:", grid_search.best_params_)

# Compute MSE on predictions
mse = mean_squared_error(y_test, predictions)
print("MSE: ", mse)

# Extract feature importances
importances = best_model.feature_importances_

# Convert the feature importances to a Series for easy plotting
importances_series = pd.Series(importances, index=joined_features.columns)

# Sort the feature importances for better visualization
sorted_importances = importances_series.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sorted_importances.plot(kind="bar")
plt.title("Feature Importances")
plt.ylabel("Importance")
plt.xlabel("Features")
plt.show()

plt.figure(figsize=(10, 6))

# No need to sort X_test since we're not plotting against a specific feature
plt.plot(
    y_test, color="black", label="Actual values", linestyle="-", marker="", linewidth=2
)
plt.plot(
    predictions,
    color="red",
    label="Predicted values",
    linestyle="-",
    marker="",
    alpha=0.7,
    linewidth=2,
)

plt.title("Random Forest Regression Predictions vs Actual")
plt.ylabel("Steering Angle")
plt.legend()
plt.show()

# Save model and scalers
model_id = str(time())
dump(best_model, model_id + "-model.joblib")
