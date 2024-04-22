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
import sysv_ipc

# numpy and cv2 are needed to access, modify, or display the pixels
import numpy
import cv2

# OD4Session is needed to send and receive messages
from opendlv import OD4Session

# Import the OpenDLV Standard Message Set.
from opendlv import opendlv_standard_message_set_v0_9_6_pb2
from predict import predict_steering_angle

global groundSteeringRequest
global angularVelocityZ
global magneticFieldZ
global accelerationY
global heading
groundSteeringRequest = 0.0
angularVelocityZ = 0.0
magneticFieldZ = 0.0
accelerationY = 0.0
heading = 0.0

session = OD4Session.OD4Session(cid=253)


# Callback function for the onGroundSteeringRequest
def onGroundSteeringRequest(msg, senderStamp, timeStamps):
    global groundSteeringRequest
    groundSteeringRequest = msg.groundSteering

def onMagnetic(msg, senderStamp, timeStamps):
    global magneticFieldZ
    magneticFieldZ = msg.magneticFieldZ


def onVelocity(msg, senderStamp, timeStamps):
    global angularVelocityZ
    angularVelocityZ = msg.angularVelocityZ


def onAccelerationY(msg, senderStamp, timeStamps):
    global accelerationY
    accelerationY = msg.accelerationY


def onHeading(msg, senderStamp, timeStamps):
    global heading
    heading = msg.heading


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
correct = 0  # N correct turns
incorrect = 0  # N incorrect turns

do_predict = False
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

    # We do not care about the prediction when angle is 0
    if groundSteeringRequest == 0.0:
        continue

    # Predict the steering angle using RF model and get the absolute value
    predicted_groundSteeringRequest = abs(
        predict_steering_angle(
            magneticFieldZ,
            accelerationY,
            angularVelocityZ,
            heading,
            "models/Tesla-feature.joblib",
            "models/Tesla-target.joblib",
            "models/Tesla.joblib",
        )
    )

    # Get the absolute value of the current wheel angle
    groundSteeringRequest = abs(groundSteeringRequest)

    # Calculate upper and lower bounds for the intervals
    lower_bound = groundSteeringRequest * 0.75
    upper_bound = groundSteeringRequest * 1.25

    # If the predicted GSR is less than upper bound but greater than lower bound
    if lower_bound <= predicted_groundSteeringRequest <= upper_bound:
        # Increment correct count
        correct += 1
    else:
        # If not, increment the incorrect count
        incorrect += 1
    # Release lock
    mutex.release()
    print("Predicted groundSteeringRequest: ", predicted_groundSteeringRequest)
    print("Actual groundSteeringRequest: ", groundSteeringRequest)
    print("Turns within OK interval (%)", correct / (correct + incorrect))
