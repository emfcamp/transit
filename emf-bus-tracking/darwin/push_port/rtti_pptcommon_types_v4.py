from dataclasses import dataclass, field
from enum import Enum

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/CommonTypes/v4"


class ToiletStatus(Enum):
    """
    The service status of a toilet in coach formation data.
    """

    UNKNOWN = "Unknown"
    IN_SERVICE = "InService"
    NOT_IN_SERVICE = "NotInService"


@dataclass
class ToiletAvailabilityType:
    """The availability of a toilet in coach formation data.

    If no availability is supplied, it should be assumed to have the
    value "Unknown".

    :ivar value:
    :ivar status: The service status of this toilet. E.g. "Unknown",
        "InService" or "NotInService".
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    status: ToiletStatus = field(
        default=ToiletStatus.IN_SERVICE,
        metadata={
            "type": "Attribute",
        },
    )
