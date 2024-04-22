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
import OD4Session
# Import the OpenDLV Standard Message Set.
import opendlv_standard_message_set_v0_9_6_pb2
import joblib
import pandas as pd

################################################################################
# This dictionary contains all distance values to be filled by function onDistance(...).
global gsr
global angular
gsr =0.0
angular=0.0
################################################################################
# This callback is triggered whenever there is a new distance reading coming in.
def onGSR(msg, senderStamp, timeStamps):
    global gsr
    gsr=msg.groundSteering

def onVelocity(msg, senderStamp, timeStamps):
    global angular
    angular=msg.angularVelocityZ



# Create a session to send and receive messages from a running OD4Session;
# Replay mode: CID = 253
# Live mode: CID = 112
# TODO: Change to CID 112 when this program is used on Kiwi.
session = OD4Session.OD4Session(cid=253)
# Register a handler for a message; the following example is listening
# for messageID 1039 which represents opendlv.proxy.DistanceReading.
# Cf. here: https://github.com/chalmers-revere/opendlv.standard-message-set/blob/master/opendlv.odvd#L113-L115
session.registerMessageCallback(1090, onGSR, opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_GroundSteeringRequest)
session.registerMessageCallback(1031, onVelocity, opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_AngularVelocityReading)
# Connect to the network session.
session.connect()

################################################################################
# The following lines connect to the camera frame that resides in shared memory.
# This name must match with the name used in the h264-decoder-viewer.yml file.
name = "/tmp/img"
# Obtain the keys for the shared memory and semaphores.
keySharedMemory = sysv_ipc.ftok(name, 1, True)
keySemMutex = sysv_ipc.ftok(name, 2, True)
keySemCondition = sysv_ipc.ftok(name, 3, True)
# Instantiate the SharedMemory and Semaphore objects.
shm = sysv_ipc.SharedMemory(keySharedMemory)
mutex = sysv_ipc.Semaphore(keySemCondition)
cond = sysv_ipc.Semaphore(keySemCondition)
correct=0
incorrect=0
################################################################################
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
    if gsr==0.0:
        continue
    
    loaded_model = joblib.load('steering_prediction_model.pkl')

    # Example: Predicting steering for a new velocity value
    new_velocity = [[angular]]  # Example new data point
    new_data = pd.DataFrame({'velocity': [angular]})

    predicted_steering = loaded_model.predict(new_data)
    predicted_steering=abs(predicted_steering[0])
    gsr=abs(gsr)
    print(gsr)
    print(predicted_steering)
    # Calculate the acceptable range, 25% above and below the target
    lower_bound = (gsr * 0.75)  # 25% less than the target
    upper_bound = (gsr * 1.25) # 25% more than the target

    # Check if the predicted steering angle falls within the acceptable range
    if lower_bound <= predicted_steering <= upper_bound:
        correct+=1
    else:
        incorrect+=1
    print("Correct: ",correct)
    print("Incorrect: ",incorrect)
    # Unlock access to shared memory.
    mutex.release()

    # Turn buf into img array (640 * 480 * 4 bytes (ARGB)) to be used with OpenCV.
    img = numpy.frombuffer(buf, numpy.uint8).reshape(480, 640, 4)

    ############################################################################
    # TODO: Add some image processing logic here.

    # The following example is adding a red rectangle and displaying the result.
    img = numpy.frombuffer(buf, numpy.uint8).reshape(480, 640, 4)

    # Make a writable copy of the image
    img_copy = img.copy()
    cv2.rectangle(img_copy, (50, 50), (100, 100), (0,0,255), 2)

    # TODO: Disable the following two lines before running on Kiwi:
    cv2.imshow("image", img_copy);
    cv2.waitKey(2);


