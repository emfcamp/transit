from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/TDData/v1"


@dataclass
class FullTdberthId:
    class Meta:
        name = "FullTDBerthID"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "length": 4,
        },
    )
    area: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 2,
        },
    )


@dataclass
class TrackingId:
    """
    Indicate a corrected Tracking ID (headcode) for a service in a TD berth.

    :ivar berth: The TD berth where the incorrectly reported train has
        been identified to be. Note that this berth is that which was
        reported to Darwin and there is no guarantee that the train is
        still in this berth at any subsequent point in time.
    :ivar incorrect_train_id: The incorrect Train ID (headcode) that is
        being reported by TD.NET.
    :ivar correct_train_id: The correct Train ID (headcode) that should
        be reported by TD.NET.
    """

    class Meta:
        name = "TrackingID"

    berth: Optional[FullTdberthId] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TDData/v1",
            "required": True,
        },
    )
    incorrect_train_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "incorrectTrainID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TDData/v1",
            "required": True,
            "length": 4,
            "pattern": r"[0-9][A-Z][0-9][0-9]",
        },
    )
    correct_train_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "correctTrainID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TDData/v1",
            "required": True,
            "length": 4,
            "pattern": r"[0-9][A-Z][0-9][0-9]",
        },
    )
