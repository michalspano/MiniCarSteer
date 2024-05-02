#!/usr/bin/env python3

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

# sysv_ipc is needed to access the shared memory where the camera image is present.

# numpy are needed to access, modify, or display the pixels
import numpy
import sysv_ipc

# OD4Session is needed to send and receive messages
from opendlv import OD4Session

# Import the OpenDLV Standard Message Set.
from opendlv import opendlv_standard_message_set_v0_9_6_pb2
from predict import predict_steering_angle,predict_turning

import os, time
import argparse

# The following command-line arguments are supported:
# (i) All LibCluon commands:
# - See https://github.com/chalmers-revere/working-with-rec-files/
# (ii) 'Custom' commands:
# --turns-only (to count only turns or no)  [default=None]
# --graph (compute a graph of the accuracy) [default=None]
# Type --help to display the expected usage.

parser = argparse.ArgumentParser(
        description='Calculate the steering angle from rec files.'
)
parser.add_argument('--cid', '-c', dest='cid', default=253, type=int,
                    help='CID of the OD4Session to send and receive messages')
parser.add_argument('--name', '-n', dest='name', default='img',
                    help='name of the shared memory area to attach')
parser.add_argument('--turns-only', '-t-o', dest='turns_only',
                    action='store_true', help='count only the turns')
parser.add_argument('--graph', '-g', dest='gen_graph',
                    action='store_true', help='generate a graph')

# Process the arguments
args = parser.parse_args()

# Store all necessary data about the car
carData = {
    "groundSteeringRequest": 0,
    "angularVelocityZ": 0,
    "magneticFieldZ": 0,
    "accelerationY": 0,
    "heading": 0,
    "correctSteeringAngle": 0,
    "incorrectSteeringAngle": 0,
    "correctWheelState": 0,
    "incorrectWheelState": 0,
    "steeringAngleAccuracy": 0.0,
    "wheelStateAccuracy": 0.0
}

# FIXME: extract the `OD4Session` configuration to a stand-alone module.
session = OD4Session.OD4Session(cid=args.cid)

# Callback function for the onGroundSteeringRequest
def onGroundSteeringRequest(msg, senderStamp, timeStamps):
    global carData
    carData["groundSteeringRequest"] = msg.groundSteering

def onMagnetic(msg, senderStamp, timeStamps):
    global carData
    carData["magneticFieldZ"] = msg.magneticFieldZ


def onVelocity(msg, senderStamp, timeStamps):
    global carData
    carData["angularVelocityZ"] = msg.angularVelocityZ


def onAccelerationY(msg, senderStamp, timeStamps):
    global carData
    carData["accelerationY"] = msg.accelerationY


def onHeading(msg, senderStamp, timeStamps):
    global carData
    carData["heading"] = msg.heading

print("Instantiating an OD4Session session.")

# Registers a handler for steering angle, velocity z, magnetic z, acceleration y, heading.
session.registerMessageCallback(
    1090,
    onGroundSteeringRequest,
    opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_GroundSteeringRequest,
)
session.registerMessageCallback(
    1031,
    onVelocity,
    opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_AngularVelocityReading,
)
session.registerMessageCallback(
    1032,
    onMagnetic,
    opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_MagneticFieldReading,
)
session.registerMessageCallback(
    1030,
    onAccelerationY,
    opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_AccelerationReading,
)
session.registerMessageCallback(
    1116,
    onHeading,
    opendlv_standard_message_set_v0_9_6_pb2.opendlv_logic_sensation_Geolocation,
)

# Connect to the network session.
session.connect()

# Location of shared memory
name = f"/tmp/{args.name}"

# Obtain the keys for the shared memory and semaphores.
keySharedMemory = sysv_ipc.ftok(name, 1, True)
keySemMutex     = sysv_ipc.ftok(name, 2, True)
keySemCondition = sysv_ipc.ftok(name, 3, True)

# Instantiate the SharedMemory and Semaphore objects.
shm   = sysv_ipc.SharedMemory(keySharedMemory)
mutex = sysv_ipc.Semaphore(keySemCondition)
cond  = sysv_ipc.Semaphore(keySemCondition)

# Relative paths to the models
turn_detection_model               = "models/Bob.joblib"
steering_prediction_model          = "models/Banana.joblib"

# Relative path to the graph-generator module
graph_gen_log = "/tmp/graph-log.csv"

# Add header, reset the file (only supported in `graph` mode)
if args.gen_graph:
    with open(graph_gen_log, "w") as f:
        f.write("timestamp;ground;predicted\n")

print("Configuration successful, waiting for an input stream...")

# Main loop to process the next image frame coming in.
# FIXME: many of these computations can be extracted to stand-alone functions.
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
    
    # Acquire shared memory
    file_meta = os.stat(name)

    # Get the last modified time
    timestamp = file_meta.st_mtime
    timestamp_ms = int(timestamp * 1000000)
        
    predicted_groundSteeringRequest = 0

    # Predict the steering angle using RF model and get the absolute value
    is_turning = predict_turning(            
        carData["magneticFieldZ"],
        carData["accelerationY"],
        carData["angularVelocityZ"],
        carData["heading"],
        turn_detection_model)

    # If turn detection detects turning we forward it to the 
    # steering prediction model
    if is_turning == 1:
        predicted_groundSteeringRequest = predict_steering_angle(
                carData["magneticFieldZ"],
                carData["accelerationY"],
                carData["angularVelocityZ"],
                carData["heading"],
                steering_prediction_model
            )
    else:
        predicted_groundSteeringRequest = 0
    
    # Append the timestamp, predicted and actual steering angles to arrays for
    # plotting. Supported in `graph` mode
    if args.gen_graph:
        with open(graph_gen_log, 'a') as f:
            # Write as a new row to the CVS file
            row = f"{timestamp};{predicted_groundSteeringRequest};{carData['groundSteeringRequest']}\n"
            f.write(row)

    """
    # Display the current timestamp and predicted steering angle
    print("group_9; ", timestamp_microseconds, "; ", predicted_groundSteeringRequest)
    """

    # Get the absolute value of the predicted steering angle
    predicted_groundSteeringRequest = abs(predicted_groundSteeringRequest)

    # Get the absolute value of the actual current wheel angle
    carData["groundSteeringRequest"] = abs(carData["groundSteeringRequest"])

    # Calculate upper and lower bounds for the intervals
    lower_bound = carData["groundSteeringRequest"] * 0.75
    upper_bound = carData["groundSteeringRequest"] * 1.25

    # Release lock
    mutex.release()
    
    # Log the values
    print("Predicted groundSteeringRequest: ", predicted_groundSteeringRequest)
    print("Actual groundSteeringRequest: ", carData["groundSteeringRequest"])
    print("Turns within OK interval (%)", carData["steeringAngleAccuracy"])
    print("Wheel state accuracy (%): ", carData["wheelStateAccuracy"])

    # Don't compute score on straights if turns only flag is active
    if carData["groundSteeringRequest"] == 0 and args.turns_only:
        continue

    # If the predicted GSR is less than upper bound but greater than lower bound
    if lower_bound <= predicted_groundSteeringRequest <= upper_bound:
        # Increment correct count
        carData["correctSteeringAngle"] += 1
    else:
        # If not, increment the incorrect count
        carData["incorrectSteeringAngle"] += 1
    
    if carData["groundSteeringRequest"] == 0 and is_turning == 0:
        carData["correctWheelState"] += 1
    elif carData["groundSteeringRequest"] != 0 and is_turning == 1:
        carData["correctWheelState"] += 1
    else:
        carData["incorrectWheelState"] += 1
    
    # Compute the percentage statistics
    carData["wheelStateAccuracy"] = (carData["correctWheelState"] /
                                     (carData["incorrectWheelState"] +
                                      carData["correctWheelState"])) * 100

    carData["steeringAngleAccuracy"] = (carData["correctSteeringAngle"] /
                                        (carData["correctSteeringAngle"] +
                                         carData["incorrectSteeringAngle"])) * 100
