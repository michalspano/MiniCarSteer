from pathlib import Path
import matplotlib.pyplot as plt
from csv import DictReader


""" 
Draws a graph of last commit prediction, this commit prediction, and actual gsr at timestamps
The function gets the video number, timestamps, actual angle, current predicted angle, and previous predicted angle
as arguments
"""
def draw_graph(rec_num, timestamps, ground_steerings, curr_predicted_steerings, prev_commit_predicted_steering):
    # Set up the size of the plot
    plt.figure(figsize=(10, 6))
    # Draw a line for actual steering angles
    plt.plot(timestamps, ground_steerings,
             label='Actual Ground Steering Request')
    # Draw a line for current steering angle predictions
    plt.plot(timestamps, curr_predicted_steerings,
             label='Current Predicted Ground Steering Request')
    # Draw a line for previous commit's steering angle predictions
    plt.plot(timestamps, prev_commit_predicted_steering,
             label='Previous Predicted Ground Steering Request')
    # X-axis has the timestamp
    plt.xlabel('sampleTime (microseconds)')
    # Y-axis are angles
    plt.ylabel('Steering angle')
    plt.title('Actual vs. Current vs. Previous Predicted Ground Steering Request')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"plot{rec_num}.png")
    plt.close()


""" 
Uses the data rom the produced files and plots the predicted steering angles and the actual steering angle 
"""
def measure_accuracy():
    # List variables used to hold the timestamps, actual ground steering, predicted ground steering
    # and previous commit predicted ground steering. These are later on plotted
    timestamps: list[int] = []
    ground_steerings: list[float] = []
    curr_predicted_steerings: list[float] = []
    prev_commit_predicted_steerings: list[float] = []

    # There are 5 videos and 5 txt files written in csv format related to each video
    # The for loop gets the data needed for plotting for one video on each iteration
    for i in range(1, 6):
        # note that for each file, we construct its, path. Then, we check if the path exists
        # Then we read its text and split them by \n and save them as float numbers for steering angles
        # And timestamps as integers
        
        # Get the timestamps for the current rec file
        # Save them in the timestamps list which is later on used to plot the graph on the x axis
        timestamp_path = Path(f"../../datasets/car{i}.timestamp.txt")
        if not timestamp_path.exists():
            raise Exception(f"Path to {timestamp_path.as_posix()} does not exist")
        timestamp_str = timestamp_path.read_text().split()
        timestamps = [int(timestamp) for timestamp in timestamp_str]

        # Get the last commit angle predictions
        prev_commit_res_path = Path(f"./previous_commit_predicted_steering.{i}.txt")
        if not prev_commit_res_path.exists():
            raise Exception(f"Path to {prev_commit_res_path.as_posix()} does not exist")
        prev_commit_predicted_steerings_str = prev_commit_res_path.read_text().split()
        prev_commit_predicted_steerings = [float(prev_commit_predicted_steering) for prev_commit_predicted_steering in prev_commit_predicted_steerings_str]

        # Get the current commit angle predictions
        curr_commit_res_path = Path(f"./curr-commit-steering.{i}.txt")
        if not curr_commit_res_path.exists():
            raise Exception(f"Path to {curr_commit_res_path.as_posix()} does not exist")
        curr_commit_predicted_steerings_str = curr_commit_res_path.read_text().split()
        curr_predicted_steerings = [float(curr_commit_predicted_steering) for curr_commit_predicted_steering in curr_commit_predicted_steerings_str]

        # Open up the file related to the current rec file. It is a csv file written in .txt
        # Extract the steering angles from the file. This is the actual steering angle
        actual_gsr = Path(f"../../datasets/car.{i}.txt")
        if not actual_gsr.exists():
                raise Exception(f"Path to {actual_gsr.as_posix()} does not exist")
        with open(f"../../datasets/car.{i}.txt", "r") as car_data_file:
            reader = DictReader(car_data_file, delimiter=",")
            for row in reader:
                ground_steerings.append(float(row["groundSteeringRequest"]))
        
        # Draw the graph that contains the actual steering angle line, the current predicted steering angle line, and
        # the previous predicted angle line, with timestamps as the x-axis unit
        draw_graph(i, timestamps, ground_steerings, curr_predicted_steerings, prev_commit_predicted_steerings)
        
        # Clear the data for the next iteration, so different videos data does not combine into one graph
        timestamps.clear()
        ground_steerings.clear()
        curr_predicted_steerings.clear()
        prev_commit_predicted_steerings.clear()


def main():
    try:
        measure_accuracy()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()