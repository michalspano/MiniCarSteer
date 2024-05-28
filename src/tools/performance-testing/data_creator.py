from pathlib import Path
import pandas as pd
from joblib import load


""" 
Create Path objects to data file for each rec file
There are 5 rec
"""
def get_file_paths() -> list[Path]:
    # A list that holds the Path objects for the rec files
    dataset: list[Path] = []
    
    # For loop used to create Path objects and save them in the path list
    # There are 5 rec files, so we have 5 paths
    for i in range(1, 6):
        dataset.append(Path(f"../../datasets/car.{i}.txt"))
  
    # return the list of paths
    return dataset


"""
Verify that The path objects made, do exist
If the path does not exist, raise an exception and mention the name of the path that does not exist
"""
def verify_path_existence(dataset: list[Path]):
    # Check if Path exists for each file
    # If a certain path does not exist, raise an exception and print an error message
    # saying which path does not exist
    for i in range(len(dataset)):
        if not dataset[i].exists():
            raise Exception(f"Path to file {dataset[i].as_posix()} does not exist.")
                

""" 
Read the data from the files and save them in a DataFrame data structure provided by pandas 
"""
def read_files_data(dataset: list[Path]) -> list[pd.DataFrame]:
    # List that holds the data_frames for each rec file
    data_frames_list: list[pd.DataFrame] = []

    # Go through the data files and save their data in a pandas DataFrame
    for i in range(len(dataset)):
        # Read The data from each file and save it in a df
        data_frames =  pd.read_csv(
            dataset[i].as_posix(),
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
            ]
        )

        # Add the df to the list of dfs
        data_frames_list.append(data_frames)
    
    # Return the list of data frames
    return data_frames_list


""" 
Use the model to predict steering angles for each fra,e of data that the data frame possesses
Save this data to a file that will be used for plotting 
"""
def predict_angle(extracted_data_frames: list[pd.DataFrame]):

    # Names of the columns of the DataFrame that is fed to the model
    required_features = ["angularVelocityX", "angularVelocityY", "angularVelocityZ", 
                         "magneticFieldX", "magneticFieldY", "magneticFieldZ", 
                         "accelerationX", "accelerationY", "accelerationZ", 
                         "heading", "pedal", "voltage", "distance"]
    
    # RF model
    model = "../../models/Thor.joblib"
    # Load the model
    rf = load(model)
    
    # Go through the data frames for each video, save the predictions for each frame in a file related to that frame
    for i in range(len(extracted_data_frames)):
        
        # Write the predicted angles in a file called curr-commit-steering.number.txt which will be used in the current and next commit for plotting
        for index, row in extracted_data_frames[i].iterrows():

            # Convert the row to DataFrame to ensure column names match those the model was trained with
            # Pass the row in a list as the model expects a 2d list
            row_df = pd.DataFrame([row], columns=required_features)
            # Predict the steering angle using the model and save the one and only prediction which is in index 0
            predicted_steering = float(rf.predict(row_df)[0])
            
            # Write the predicted steering angle in a file which will be used for the next and current commit plotting
            # If the file does not exist, create it. Otherwise, append do it
            curr_commit_path = Path(f"curr-commit-steering.{i + 1}.txt")
            # Mode to open the file. If it does not exist, use 'x' which means a new file will be created
            # If file exists, use 'a' which means file is opened in append mode
            mode = "x" if not curr_commit_path.exists() else "a"
            with open(f"curr-commit-steering.{i + 1}.txt", mode) as curr_predicted_steering:
                curr_predicted_steering.write(str(predicted_steering) + "\n")


def main():
    try:
        file_paths: list[Path] = get_file_paths()
        verify_path_existence(file_paths)
        extracted_data: list[pd.DataFrame] = read_files_data(file_paths)
        predict_angle(extracted_data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()