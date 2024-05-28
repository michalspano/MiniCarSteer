import numpy as np
import pandas as pd
import joblib

def predict_steering_angle(carData, model):
    # Load the RF model
    rf = joblib.load(model)

    # Ensure 'carData' is a dictionary with all necessary keys corresponding to the features
    required_features = ["angularVelocityX", "angularVelocityY", "angularVelocityZ", 
                         "magneticFieldX", "magneticFieldY", "magneticFieldZ", 
                         "accelerationX", "accelerationY", "accelerationZ", 
                         "heading", "pedal", "voltage", "distance"]
                         
    # Create a list of feature values in the correct order
    feature_values = [carData[feature] for feature in required_features]
    
    # Convert the list of feature values into a 2D list as expected by the model
    X = [feature_values]

    # Convert to DataFrame to ensure column names match those the model was trained with
    X_df = pd.DataFrame(X, columns=required_features)
    
    # Generate predictions from the input features
    y_pred = rf.predict(X_df)
    
    # Return the first (and only) prediction from the list
    return y_pred[0]