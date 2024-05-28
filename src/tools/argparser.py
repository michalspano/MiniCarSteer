"""
Project: DIT639 Project
File: src/tools/argparser.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: A custom wrapper around the argparse library for our application.
"""

import argparse

"""
Initializes the argument parser with the default values. This function is used
to parse the command line arguments for the application.
"""
def argparser_init():
    parser = argparse.ArgumentParser(
        description="Calculate the steering angle from rec files with ML, based"
        + " on the Chalmers ReVeRe Project."
    )
    parser.add_argument(
        "--cid", "-c",
        dest="cid",
        default=253,
        type=int,
        help="CID of the OD4Session to send and receive messages",
    )
    parser.add_argument(
        "--name", "-n",
        dest="name",
        default="img",
        help="name of the shared memory area to attach",
    )
    parser.add_argument(
        "--model", "-m",
        dest="model",
        default="Thor.joblib",
        type=str,
        help=f"select a joblib based model to predict the steering angle;" 
              + " acquired from ./models/<NAME>",
    )
    parser.add_argument(
        "--graph", "-g", dest="gen_graph", action="store_true", help="generate a graph"
    )
    parser.add_argument(
        "--verbose", "-v", dest="verbose", action="store_true", help="enable debug window and additional metrics"
    )
    parser.add_argument(
        "--dev-mode", "-d-m", dest="dev_mode",
        action="store_true", help="calculate and show accuracy on only turns",
    )

    # Process the arguments and return
    return parser.parse_args()
