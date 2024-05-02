import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
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
}


# Initialize empty DataFrames for features and target
joined_features = pd.DataFrame(
    columns=["magneticFieldZ", "accelerationY", "angularVelocityZ", "heading"]
)
joined_targets = pd.DataFrame(columns=["steering"])

# Loop through the files for 6 cars
for i in range(1, 7):  # 1 to 6 inclusive
    # Setup the paths to read from
    steering_file = f"../datasets/nonzero/car.{i}.steering.txt"
    magneticZ_file = f"../datasets/nonzero/car.{i}.mag.z.txt"
    accelerationY_file = f"../datasets/nonzero/car.{i}.acceleration.y.txt"
    velocityZ_file = f"../datasets/nonzero/car.{i}.velocity.z.txt"
    heading_file = f"../datasets/nonzero/car.{i}.heading.txt"

    # Read datasets into dataframes
    steering = pd.read_csv(steering_file, names=["steering"])
    magneticZ = pd.read_csv(magneticZ_file, names=["magneticFieldZ"])
    accelerationY = pd.read_csv(accelerationY_file, names=["accelerationY"])
    velocityZ = pd.read_csv(velocityZ_file, names=["angularVelocityZ"])
    heading = pd.read_csv(heading_file, names=["heading"])
    if (
        len(steering) == 0
        or len(magneticZ) == 0
        or len(accelerationY) == 0
        or len(velocityZ) == 0
        or len(heading) ==0
    ):
        raise Exception("0 Length df encountered")
    # Concatenate dataframes into single feature set
    features = pd.concat([magneticZ, accelerationY, velocityZ, heading], axis=1)

    # Concatenate dataframes with previous dataframes
    joined_features = pd.concat([joined_features, features], axis=0, ignore_index=True)
    joined_targets = pd.concat([joined_targets, steering], axis=0, ignore_index=True)


X = joined_features
y = joined_targets.values.reshape(
    -1, 1
)  # We need to reshape this into a 2D array since train_test_split expects 2D array

# Split X input and target y into their respective datasets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Setup scalers
X_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()

# Scale X input
X_train_scaled = X_scaler.fit_transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

# Scale targets
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

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

# Train model with Grid Search using scaled inputs and targets
grid_search.fit(X_train_scaled, y_train_scaled.ravel())


best_model = grid_search.best_estimator_
predictions_scaled = best_model.predict(X_test_scaled)
print("Best Parameters:", grid_search.best_params_)

# Inverse transform predictions to get them back on the original target scale
predictions = y_scaler.inverse_transform(predictions_scaled.reshape(-1, 1))

# Compute MSE on predictions
mse = mean_squared_error(y_test, predictions)
print("MSE: ", mse)

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
model_id = str(time.time())
joblib.dump(best_model, model_id + "-model.joblib")
joblib.dump(X_scaler, model_id + "-feature-scaler.joblib")
joblib.dump(y_scaler, model_id + "-targets-scaler.joblib")
