"""
File: src/opendlv/OD4Session_init.py
Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström
Description: A custom wrapper around the OD4Session class to initialize the session
             with the required callback functions and message types.
"""

from opendlv import OD4Session
from opendlv import OD4callback as callback
from opendlv import opendlv_standard_message_set_v0_9_6_pb2

"""
Initilize the OD4Session with the required message types and callback functions.
The following API is used to register the message types and callback functions:
    - 1090: GroundSteeringRequest
    - 1031: AngularVelocityReading
    - 1032: MagneticFieldReading
    - 1030: AccelerationReading
    - 1116: Geolocation
    - 1086: PedalPositionRequest
    - 1037: VoltageReading
    - 1039: DistanceReading
This function enables the user to specify the custom ports for the message types.
@Example:
    OD4Session_init(cid, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018)
"""
def OD4Session_init(cid, *ports):
    session = OD4Session.OD4Session(cid=cid)

    session.registerMessageCallback(
        1090 if not ports else ports[0],
        callback.onGroundSteeringRequest,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_GroundSteeringRequest,
    )
    session.registerMessageCallback(
        1031 if not ports else ports[1],
        callback.onVelocity,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_AngularVelocityReading,
    )
    session.registerMessageCallback(
        1032 if not ports else ports[2],
        callback.onMagnetic,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_MagneticFieldReading,
    )
    session.registerMessageCallback(
        1030 if not ports else ports[3],
        callback.onAccelerationY,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_AccelerationReading,
    )
    session.registerMessageCallback(
        1116 if not ports else ports[4],
        callback.onHeading,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_logic_sensation_Geolocation,
    )
    session.registerMessageCallback(
        1086 if not ports else ports[5],
        callback.onPedal,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_PedalPositionRequest,
    )

    session.registerMessageCallback(
        1037 if not ports else ports[6],
        callback.onVoltage,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_VoltageReading,
    )
    session.registerMessageCallback(
        1039 if not ports else ports[7],
        callback.onDistance,
        opendlv_standard_message_set_v0_9_6_pb2.opendlv_proxy_DistanceReading,
    )
    
    # Establish a connection
    session.connect()

