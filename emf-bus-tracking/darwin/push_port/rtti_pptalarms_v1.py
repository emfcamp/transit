from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1"


@dataclass
class RttialarmData:
    """
    Type describing each type of alarm that can be set.

    :ivar td_area_fail: Alarm for a single TD area failure. Contents
        identify the failed area code.
    :ivar td_feed_fail: Alarm for the failure of the entire TD feed into
        Darwin.
    :ivar tyrell_feed_fail: Alarm for the failure of the Tyrell feed
        into Darwin.
    :ivar id: Unique identifier for this alarm
    """

    class Meta:
        name = "RTTIAlarmData"

    td_area_fail: Optional[str] = field(
        default=None,
        metadata={
            "name": "tdAreaFail",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1",
            "length": 2,
        },
    )
    td_feed_fail: Optional[object] = field(
        default=None,
        metadata={
            "name": "tdFeedFail",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1",
        },
    )
    tyrell_feed_fail: Optional[object] = field(
        default=None,
        metadata={
            "name": "tyrellFeedFail",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Rttialarm:
    """
    An update to a Darwin alarm.

    :ivar set: Set a new alarm.
    :ivar clear: Clear an existing alarm. The contents identify the
        unique alarm identifier that has been cleared.
    """

    class Meta:
        name = "RTTIAlarm"

    set: Optional[RttialarmData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1",
        },
    )
    clear: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Alarms/v1",
        },
    )
