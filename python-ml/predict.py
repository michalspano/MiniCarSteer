import numpy as np
import pandas as pd
import joblib


def predict_steering_angle(
    magneticFieldZ, accelerationY, angularVelocityZ, heading, X_scaler, y_scaler, model
):
    # Load the previous scalers
    X_scaler = joblib.load(X_scaler)
    y_scaler = joblib.load(y_scaler)

    # Load the RF model
    rf = joblib.load(model)

    # Create X inputs
    X = pd.DataFrame(
        [[magneticFieldZ, accelerationY, angularVelocityZ, heading]],
        columns=["magneticFieldZ", "accelerationY", "angularVelocityZ", "heading"],
    )

    # Scale X inputs in accordance to X scaler params
    X_scaled = X_scaler.transform(X)

    # Generate targets from X inputs
    y = rf.predict(X_scaled)

    # Perform inverse transformation on target y
    predicted_steering_angle = y_scaler.inverse_transform(
        y.reshape(-1, 1) # Reshape as this is a single feature and inverse transform expects 2D array
    )

    # Return steering wheel angle
    return predicted_steering_angle[0][0]
