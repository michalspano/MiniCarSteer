from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Initialize a scaler
scaler = MinMaxScaler(feature_range=(0, 1))
steeringAvgScaleFactor=0
angularAvgScaleFactor=0
# Loop through the range of x values
for x in range(1, 7):
    try:
        # Construct the filenames
        steering_filename = f'car.{x}.steering.txt'
        velocity_filename = f'car.{x}.velocity.txt'
        
        # Load the data
        steering_data = pd.read_csv(steering_filename, names=['angle'])
        velocity_data = pd.read_csv(velocity_filename, names=['Z'])
        
        # Ensure matching lengths
        if len(steering_data) != len(velocity_data):
            raise Exception(f"Mismatch in data lengths for car {x}")
        
        # Let's choose to merge on index assuming the rows correspond to the same timestamps
        merged_data = pd.concat([velocity_data, steering_data['angle']], axis=1)
        
        # Fit the scaler to the data
        scaler.fit(merged_data)
        
        # Output the scaling factors for Z (angular velocity) and angle (steering)
        print(f"Car {x} Scaling Factors:")
        print("Angular Velocity (Z):", scaler.scale_[0])
        print("Steering Angle:", scaler.scale_[1], "\n")
        angularAvgScaleFactor+=scaler.scale_[0]
        steeringAvgScaleFactor+=scaler.scale_[1]
    except FileNotFoundError as e:
        print(f"File not found for car {x}: {e}")
print(f"Avg scale factor angular velocity (Z): {(angularAvgScaleFactor/6)}")
print(f"Avg scale factor stering: {(steeringAvgScaleFactor/6)}")