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
import sysv_ipc, sys
# numpy and cv2 are needed to access, modify, or display the pixels
import numpy, cv2
import matplotlib.pyplot as plt

# OD4Session is needed to send and receive messages
from opendlv import OD4Session

# Import the OpenDLV Standard Message Set.
from opendlv import opendlv_standard_message_set_v0_9_6_pb2
from predict import predict_steering_angle,predict_turning

import os
import time

global carData
carData={
    "groundSteeringRequest":0,
    "angularVelocityZ":0,
    "magneticFieldZ":0,
    "accelerationY":0,
    "heading":0,
    "correctSteeringAngle":0,
    "incorrectSteeringAngle":0,
    "correctWheelState":0,
    "incorrectWheelState":0,
    "steeringAngleAccuracy":0,
    "wheelStateAccuracy":0
}

session = OD4Session.OD4Session(cid=253)

# Arrays to store all the timestamps and steering angles from one video
timestamps = []
ground_steering_requests = []
predicted_steering_requests = []

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
name = "/tmp/img"

# Obtain the keys for the shared memory and semaphores.
keySharedMemory = sysv_ipc.ftok(name, 1, True)
keySemMutex = sysv_ipc.ftok(name, 2, True)
keySemCondition = sysv_ipc.ftok(name, 3, True)


# Instantiate the SharedMemory and Semaphore objects.
shm = sysv_ipc.SharedMemory(keySharedMemory)
mutex = sysv_ipc.Semaphore(keySemCondition)
cond = sysv_ipc.Semaphore(keySemCondition)

turn_detection_model="models/Hildegard.joblib"
turn_detection_scaler="models/Hildegard-feature.joblib"

steering_prediction_model="models/Tesla.joblib"
steering_prediction_feature_scaler="models/Tesla-feature.joblib"
steering_prediction_target_scaler="models/Tesla-target.joblib"

# System flags
turns_only = "--turns-only" in sys.argv


# Main loop to process the next image frame coming in.
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
    timestamp  = file_meta.st_mtime
    timestamp_microseconds = int(timestamp * 1000000)
    # Add the timestamp to this video's timestamp array for plotting
    timestamps.append(timestamp_microseconds)
    
    predicted_groundSteeringRequest=0
    # Predict the steering angle using RF model and get the absolute value
    is_turning=predict_turning(            
        carData["magneticFieldZ"],
        carData["accelerationY"],
        carData["angularVelocityZ"],
        carData["heading"],
        turn_detection_scaler,
        turn_detection_model)

    # If turn detection detects turning we forward it to the 
    # steering prediction model
    if is_turning==1:
        predicted_groundSteeringRequest = predict_steering_angle(
                carData["magneticFieldZ"],
                carData["accelerationY"],
                carData["angularVelocityZ"],
                carData["heading"],
                steering_prediction_feature_scaler,
                steering_prediction_target_scaler,
                steering_prediction_model
            )
    else:
        predicted_groundSteeringRequest=0
    
    # Append the predicted and actual steering angles to arrays for plotting
    predicted_steering_requests.append(predicted_groundSteeringRequest)
    ground_steering_requests.append(carData["groundSteeringRequest"])

    # Display the current timestamp and predicted steering angle
    print("group_9; ", timestamp_microseconds, "; ", predicted_groundSteeringRequest)

    # Get the absolute value of the predicted steering angle
    predicted_groundSteeringRequest = abs(predicted_groundSteeringRequest)

    # Get the absolute value of the actual current wheel angle
    carData["groundSteeringRequest"] = abs(carData["groundSteeringRequest"])

    # Calculate upper and lower bounds for the intervals
    lower_bound = carData["groundSteeringRequest"] * 0.75
    upper_bound = carData["groundSteeringRequest"] * 1.25

    # Release lock
    mutex.release()
    
    #print("Predicted groundSteeringRequest: ", predicted_groundSteeringRequest)
    #print("Actual groundSteeringRequest: ", carData["groundSteeringRequest"])
    #print("Turns within OK interval (%)", carData["steeringAngleAccuracy"])
    #print("Wheel state accuracy (%): ",carData["wheelStateAccuracy"])

    # Dont compute score on straights if turns only flag is active
    if carData["groundSteeringRequest"]==0 and turns_only:
        continue
    # If the predicted GSR is less than upper bound but greater than lower bound
    if lower_bound <= predicted_groundSteeringRequest <= upper_bound:
        # Increment correct count
        carData["correctSteeringAngle"] += 1
    else:
        # If not, increment the incorrect count
        carData["incorrectSteeringAngle"] += 1
    
    if carData["groundSteeringRequest"]==0 and is_turning==0:
        carData["correctWheelState"]+=1
    elif carData["groundSteeringRequest"]!=0 and is_turning==1:
        carData["correctWheelState"]+=1
    else:
        carData["incorrectWheelState"]+=1

    carData["wheelStateAccuracy"]=(carData["correctWheelState"] / (carData["incorrectWheelState"] + carData["correctWheelState"]))*100

    carData["steeringAngleAccuracy"]=(carData["correctSteeringAngle"] / (carData["correctSteeringAngle"] + carData["incorrectSteeringAngle"]))*100
    
    # Plot a graph to compare actual and predicted steering angle
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, ground_steering_requests, label='Actual Ground Steering Request')
    plt.plot(timestamps, predicted_steering_requests, label='Predicted Ground Steering Request')
    plt.xlabel('sampleTime (microseconds)')
    plt.ylabel('Steering angle')
    plt.title('Actual vs. Predicted Ground Steering Request')
    plt.legend()
    plt.grid(True)
    plt.savefig('plot.png')
    plt.close()