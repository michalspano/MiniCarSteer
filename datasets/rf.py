import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib.pyplot as plt

# Initialize a list to hold DataFrames
data_frames = []

# Loop to read and combine data
for x in range(1, 2):
    try:
        print(x)
        steering_filename = f'car.{x}.steering.txt'
        velocity_filename = f'car.{x}.velocity.txt'
        
        steering_data = pd.read_csv(steering_filename, names=['steering_angle'])
        velocity_data = pd.read_csv(velocity_filename, names=['velocity'])
        
        # Validate data lengths
        if len(steering_data) != len(velocity_data):
            raise Exception(f"Mismatch in data lengths for car {x}")
        
        # Combining velocity and steering data into a single DataFrame
        combined_data = pd.concat([velocity_data, steering_data], axis=1)
        data_frames.append(combined_data)
    except FileNotFoundError as e:
        print(f"File not found for car {x}: {e}")

# Concatenating all data frames in the list into a single DataFrame
all_data = pd.concat(data_frames, ignore_index=True)

# Splitting data into features (X) and the target variable (y)
X = all_data[['velocity']]
y = all_data['steering_angle']

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Random Forest Regressor
rf = RandomForestRegressor(n_estimators=50,max_depth=5)

# Train the model
rf.fit(X_train, y_train)

# Predict on the testing set
y_pred = rf.predict(X_test)

# Evaluate the model with Mean Squared Error
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Save the model to disk
joblib.dump(rf, 'steering_prediction_model.pkl')

print("Model saved successfully!")


# Plotting Actual vs. Predicted
plt.figure(figsize=(10, 6))  # Set figure size
plt.scatter(X_test, y_test, color='black', label='Actual')  # Plot actual values
plt.scatter(X_test, y_pred, color='green', alpha=0.5, label='Predicted')  # Plot predicted values
plt.title('Actual vs Predicted Steering Angles')  # Title of the plot
plt.xlabel('Velocity')  # X-axis label
plt.ylabel('Steering Angle')  # Y-axis label
plt.legend()  # Show legend
plt.savefig('plot.png')  # Saves the plot as a PNG