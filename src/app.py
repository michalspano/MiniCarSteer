#!/usr/bin/env python3

"""
File: src/app.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: The entry point of the application.
"""

# Copyright (C) 2018 Christian Berger
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Import required depdendencies
import sysv_ipc
import tkinter as tk
from queue import Queue
from copy import deepcopy
from threading import Thread
from os import environ, stat, path

# Import custom utility modules
from tools import *
from frameData import frameData
from predict import predict_steering_angle
from opendlv.OD4Session_init import OD4Session_init

"""
This function processes a frame from the queue and sends it to the RF model_id
to predict the steering wheel angle.
"""
def queue_processor():
    # Contains metadata used for calculating accuracy
    # as well as the accuracy itself
    accuracy = {
        "correctSteeringAngle": 0,
        "incorrectSteeringAngle": 0,
        "steeringAngleAccuracy": 0.0,
    }

    while True: # continue indefinitely in the thread
        # Wait until we get a new frame to process
        # code execution in this function is blocked until then
        frame = dataQueue.get()

        # Get the last modified time from the metadata of the file
        timestamp = stat(name).st_mtime

        # Predict steering angle on this frame
        predicted_groundSteeringRequest = predict_steering_angle(
            frame, steering_prediction_model
        )

        # Append the timestamp, predicted and actual steering angles to arrays for
        # plotting. Supported in `graph` mode
        if args.gen_graph:
            write_log_row(timestamp, predicted_groundSteeringRequest,
                          frame['groundSteeringRequest'])

        # In development mode, calculate the accuracy of GSR and log it. Otherwise,
        # skip the iteration, after printing timestamp of the frame, the predicted steering angle
        # and the actual steering angle
        if not args.dev_mode:
            # Display the current timestamp and predicted steering angle
            # The timestamp is, inside the function, converted to microseconds.
            log_frame(timestamp, predicted_groundSteeringRequest)
            continue

        # Don't compute score on straights
        if frame["groundSteeringRequest"] == 0:
            continue

        # If the predicted GSR is less than upper bound but greater than lower bound
        if is_within_bounds(predicted_groundSteeringRequest, frame["groundSteeringRequest"]):
            # Increment correct count
            accuracy["correctSteeringAngle"] += 1
        else:
            # If not, increment the incorrect count
            accuracy["incorrectSteeringAngle"] += 1

        # In the development mode, log additional statistics to the console
        debug_performance(predicted_groundSteeringRequest,
                          frame["groundSteeringRequest"],
                          accuracy["steeringAngleAccuracy"])
    
        # Update the state of the accuracy per frame
        accuracy["steeringAngleAccuracy"] = compute_percentage(
                accuracy["correctSteeringAngle"], accuracy["incorrectSteeringAngle"])


# The main entry file of the program
if __name__ == "__main__":
    # Detect if there is a graphical user interface available
    GUI_AVAILABLE = "DISPLAY" in environ # (LLM: 10.txt)

    # Call the argparser to initialize the command-line interface component.
    args = argparser_init()

    # Instantiate a queue to process the frames
    dataQueue = Queue()

    # Process the selected model path
    steering_prediction_model = f"models/{args.model}"

    # Verify that the model exists
    if not path.exists(steering_prediction_model):
        print(f"Error: Model {steering_prediction_model} not found.")
        exit(1)

    print(f"> Selected model: {steering_prediction_model}")
    
    ## LOG ##
    print("> Instantiating an OD4Session session...")

    # Connect to the network OD4Session. If this fails, `OD4Session_init` exits
    # the program.
    OD4Session_init(args.cid)

    ## LOG ##
    print("> OD4Session established.")
    print("> Configuring the shared memory...")

    # Location of shared memory
    name = f"/tmp/{args.name}"

    # As the shared memory folder may not exist, we put this block in a try except block to
    # any file exceptions and print the exception message
    try:
        # Obtain the keys for the shared memory and semaphores.
        keySharedMemory = sysv_ipc.ftok(name, 1, True)
        keySemMutex     = sysv_ipc.ftok(name, 2, True)
        keySemCondition = sysv_ipc.ftok(name, 3, True)
    except Exception as e:
        print(f"{e} named {name}")
        exit(1)

    # Instantiate the SharedMemory and Semaphore objects.
    shm   = sysv_ipc.SharedMemory(keySharedMemory)
    mutex = sysv_ipc.Semaphore(keySemCondition)
    cond  = sysv_ipc.Semaphore(keySemCondition)

    # Add header, reset the file (only supported in `graph` mode)
    reset_graph_data() if args.gen_graph else None

    ## LOG ##
    print("> Configuration successful, waiting for an input stream...")

    # Open a debug window (only supported in `verbose` mode if there is a GUI
    # available).
    # FIXME: may sometimes yield 'fontconfig error: no writable cache
    # directory' (this error is not detrimental). Treat it as a warning.
    root = verbose_text = None
    if args.verbose and GUI_AVAILABLE:
        root = tk.Tk()
        root.title("Debug window")
        verbose_text = tk.Text(root)
        verbose_text.pack()
        verbose_text.insert(tk.END, "Verbose mode is enabled.")
        root.update()  # Update the window
        print("> Debug window started.") ## LOG ##

    # Start a new daemon thread (kill it when main thread exits)
    worker = Thread(target=queue_processor, daemon=True)

    # Start the worker thread
    worker.start()

    while True:
        # Wait for next notification.
        cond.Z()
        # Lock access to shared memory.
        mutex.acquire()
        # Attach to shared memory.
        shm.attach()
        # Read shared memory into own buffer.
        buf = shm.read()
        # Detach to shared memory.
        shm.detach()

        # Create a deep copy of the current frame and queue it for processing
        dataQueue.put(deepcopy(frameData))
        
        # Continue to display the `verbose` window
        if args.verbose and GUI_AVAILABLE and verbose_text:
            # Get metadata from the shared mem file
            file_meta = stat(name)

            # Get the last modified time
            timestamp_ms = int(file_meta.st_mtime * 1000000)

            # Display the data that was used to train the model in a separate window for debugging.
            formatted_data = format_data_as_string(
                    Timestamp=timestamp_ms,
                    Magnetic_field_Z=frameData["magneticFieldZ"],
                    Magnetic_field_Y=frameData["magneticFieldY"],
                    Magnetic_field_X=frameData["magneticFieldX"],
                    Angular_Velocity_Z=frameData["angularVelocityZ"],
                    Angular_Velocity_Y=frameData["angularVelocityY"],
                    Angular_Velocity_X=frameData["angularVelocityX"],
                    Acceleration_Y=frameData["accelerationY"],
                    Acceleration_X=frameData["accelerationX"],
                    Acceleration_Z=frameData["accelerationZ"],
                    Heading=frameData["heading"],
                    Pedal=frameData["pedal"],
                    Voltage=frameData["voltage"],
                    Distance=frameData["distance"]
            )

            # Insert the formatted data into the text widget
            verbose_text.insert(tk.END, formatted_data)
            
            root.update() if root else None # Update the window
            verbose_text.see(tk.END)        # Scroll to the bottom

        # Release the mutex
        mutex.release()
