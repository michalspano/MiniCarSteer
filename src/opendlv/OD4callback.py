"""
Project: DIT639 Project
File: src/opendlv/OD4callback.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: The callback functions for the OpenDLV messages.
"""

from frameData import frameData # Import the shared dictionary

def onGroundSteeringRequest(msg, senderStamp, timeStamps):
    global frameData
    frameData["groundSteeringRequest"] = msg.groundSteering


def onMagnetic(msg, senderStamp, timeStamps):
    global frameData
    frameData["magneticFieldZ"] = msg.magneticFieldZ
    frameData["magneticFieldY"] = msg.magneticFieldY
    frameData["magneticFieldX"] = msg.magneticFieldX


def onVelocity(msg, senderStamp, timeStamps):
    global frameData
    frameData["angularVelocityZ"] = msg.angularVelocityZ
    frameData["angularVelocityY"] = msg.angularVelocityY
    frameData["angularVelocityX"] = msg.angularVelocityX


def onAccelerationY(msg, senderStamp, timeStamps):
    global frameData
    frameData["accelerationY"] = msg.accelerationY
    frameData["accelerationX"] = msg.accelerationX
    frameData["accelerationZ"] = msg.accelerationZ


def onHeading(msg, senderStamp, timeStamps):
    global frameData
    frameData["heading"] = msg.heading


def onPedal(msg, senderStamp, timeStamps):
    global frameData
    frameData["pedal"] = msg.position


def onVoltage(msg, senderStamp, timeStamps):
    global frameData
    frameData["voltage"] = msg.voltage


def onDistance(msg, senderStamp, timeStamps):
    global frameData
    frameData["distance"] = msg.distance

