"""
File: src/tools/utils.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: A set of constants, utility functions for the system.
"""

# Absolute path to the graph-generator data file
from decimal import DivisionByZero


### Constants ###

graph_gen_log = "/tmp/graph-log.csv"

### Functions ###

"""
A function to determine whether the prediceted value is within the allowed error range.
Covered in: ./src/tests/test_utils.py
"""
def is_within_bounds(predicted, actual, error=0.25):
    if not (0 <= error <= 1):
        raise Exception('The allowed error range is 0-1.')

    # Default behavior (whenever `actual` is non-negative)
    lower_bound, upper_bound = actual * (1 - error), actual * (1 + error)

    # Negative `actual` value, invert the logic
    if actual < 0:
        lower_bound, upper_bound = actual * (1 + error), actual * (1 - error)
    
    # Determine the interval and check if the predicted value is within the bounds
    return lower_bound <= predicted <= upper_bound


"""
Round to two decimal numbers (default)
Covered in: ./src/tests/test_utils.py
"""
def compute_percentage(correct, incorrect, precision=2):
    if correct + incorrect == 0:
        raise DivisionByZero('Cannot divide by zero.')
    return round((correct / (correct + incorrect)) * 100, precision)


"""
Write a new row entry to graph_gen_log. Used in `graph` mode
Covered in: ./src/tests/test_utils.py
"""
def write_log_row(timestamp, ground, predicted, path=graph_gen_log):
    with open(path, 'a') as f:
        row = f"{timestamp};{ground};{predicted}\n"
        f.write(row)


"""
Reset the graph_gen_log file. Used in `graph` mode.
Covered in: ./src/tests/test_io.py
"""
def reset_graph_data(path=graph_gen_log, verbose=True):
    with open(path, "w") as f:
        f.write("timestamp;ground;predicted\n")
    if verbose: # display msg if verbose is set
        print(f"> The file {path} has been reset.")


"""
Debug the performance of the strategy.
Covered in: ./src/tests/test_utils.py
"""
def debug_performance(*args):
    print("Predicted groundSteeringRequest:", args[0])
    print("Actual groundSteeringRequest:", args[1])
    print("Turns within OK interval (%)", args[2])


"""
Log each frame to the console. The format is followed from A24.
The timestamp is converted to microseconds (*10^6).
Covered in: ./src/tests/test_utils.py
"""
def log_frame(timestamp, value, group_nr=9):
    print(f"group_{group_nr};{int(timestamp * 1_000_000)};{value}")


"""
Helper function to format all features to display in a debug/verbose window.
Covered in: ./src/tests/test_utils.py
"""
def format_data_as_string(**kwargs):
    formatted_text = ""
    for key, value in kwargs.items():
        # Replace underscores with a whitespaces for the keys
        key = key.replace("_", " ")
        formatted_text += f"{key}: {value}\n"
    return formatted_text + "\n"

