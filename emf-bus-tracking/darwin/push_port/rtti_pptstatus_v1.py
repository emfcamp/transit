from dataclasses import dataclass, field
from typing import Dict, Optional

__NAMESPACE__ = "http://thalesgroup.com/RTTI/PushPortStatus/root_1"


@dataclass
class Ppconnect:
    """
    Signal end of the setup phase and switch to use the requested PP data schema.
    """

    class Meta:
        name = "PPConnect"
        namespace = "http://thalesgroup.com/RTTI/PushPortStatus/root_1"


@dataclass
class PpreqVersion:
    """
    Request the schema versions required by the client.

    :ivar version: The namespace of the Push Port data schema supported
        by the client.
    :ivar ttversion: The namespace of the Push Port Timetable schema
        supported by the client.
    :ivar ttrefversion: The namespace of the Push Port Timetable
        Reference data schema supported by the client.
    """

    class Meta:
        name = "PPReqVersion"
        namespace = "http://thalesgroup.com/RTTI/PushPortStatus/root_1"

    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
        },
    )
    ttversion: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
        },
    )
    ttrefversion: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
        },
    )


@dataclass
class StatusType:
    """
    Status Code Type.
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 128,
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 32,
        },
    )
    any_attributes: Dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        },
    )


@dataclass
class Ppstatus(StatusType):
    """
    Setup phase status/heartbeat response.
    """

    class Meta:
        name = "PPStatus"
        namespace = "http://thalesgroup.com/RTTI/PushPortStatus/root_1"
