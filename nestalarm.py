import config
import socket
import requests
import uuid
from datetime import datetime
from nest.trait.occupancy_pb2 import StructureModeTrait
from nestlabs.gateway.v1_pb2 import ResourceCommand, ResourceCommandRequest, ResourceRequest
from weave.common_pb2 import ResourceId
from google.protobuf.any_pb2 import Any


def setNestMode(mode):
    # Build request
    command = Any()
    command.Pack(StructureModeTrait.StructureModeChangeRequest(
        structureMode=mode,
        reason=StructureModeTrait.StructureModeReason.STRUCTURE_MODE_REASON_EXPLICIT_INTENT,
        userId=ResourceId(resourceId=config.NEST_USER_ID)
    ), "type.nestlabs.com")
    request = ResourceCommandRequest(
        resourceRequest=ResourceRequest(
            resourceId=f"STRUCTURE_{config.NEST_STRUCTURE_ID}",
            requestId=str(uuid.uuid4()),
        ),
        resourceCommands=[ResourceCommand(
            traitLabel="structure_mode",
            command=command,
        )]
    )
    request = request.SerializeToString()

    # Send request
    response = requests.post(
        url=config.NEST_ENDPOINT,
        data=request,
        headers={
            "Authorization": f"Basic {config.NEST_ACCESS_TOKEN}".encode("utf-8"),
            "Content-Type": "application/x-protobuf",
            "User-Agent": config.NEST_USER_AGENT,
            "X-Accept-Response-Streaming": "true",
        },
    )

    # Check if response succeeded
    if response.status_code != requests.codes.ok or not "StructureModeChangeRespons" in response.text:
        print(f"{datetime.now()} WARNING: Failed to set nest mode")
        print(f"Status code: {response.status_code}")
        print(response.text)


# Login to alarm
alarm = socket.create_connection((config.ALARM_IP, config.ALARM_PORT))
alarm.recv(1024)
alarm.send(f"{config.ALARM_PASSWORD}\r\n".encode("ascii"))
alarm.recv(1024)

# Get initial alarm state
lastAlarmState = ""
while not "****" in lastAlarmState:
    lastAlarmState = str(alarm.recv(1024))

# Listen for changes in alarm state and then update nest mode
while True:
    currentAlarmState = str(alarm.recv(1024))
    if "AWAY" in currentAlarmState and not "AWAY" in lastAlarmState:
        setNestMode(StructureModeTrait.StructureMode.STRUCTURE_MODE_HOME)
    elif "DISARMED" in currentAlarmState and not "DISARMED" in lastAlarmState:
        setNestMode(StructureModeTrait.StructureMode.STRUCTURE_MODE_AWAY)
    lastAlarmState = currentAlarmState
