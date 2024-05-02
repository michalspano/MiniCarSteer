#!/usr/bin/env python3

from csv import DictReader
import matplotlib.pyplot as plt

# Source of the parameters
graph_data_src = "/tmp/graph-log.csv"

timestamps         = []
ground_steering    = []
predicted_steering = []

# Plot a graph to compare actual and predicted steering angle.
def main():
    # Open the CSV file, read the captured values
    with open(graph_data_src, "r") as csvfile:
        reader = DictReader(csvfile, delimiter=";")
        for row in reader:
            timestamps.append(float(row['timestamp']))
            ground_steering.append(float(row['ground']))
            predicted_steering.append(float(row['predicted']))
    
    # Create the graph, take the predicted and group angles as two
    # subplots.
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, ground_steering,
             label='Actual Ground Steering Request')

    plt.plot(timestamps, predicted_steering,
             label='Predicted Ground Steering Request')

    plt.xlabel('sampleTime (microseconds)')
    plt.ylabel('Steering angle')
    plt.title('Actual vs. Predicted Ground Steering Request')
    plt.legend()
    plt.grid(True)
    plt.savefig('plot.png')
    plt.close()

if __name__ == '__main__':
    main()
