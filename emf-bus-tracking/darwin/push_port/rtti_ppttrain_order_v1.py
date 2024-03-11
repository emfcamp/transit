from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1"


@dataclass
class TrainOrderItem:
    """
    Describes the identifier of a train in the train order.

    :ivar rid: For trains in the train order where the train is the
        Darwin timetable, it will be identified by its RID
    :ivar train_id: Where a train in the train order is not in the
        Darwin timetable, a Train ID (headcode) will be supplied
    """

    rid: Optional["TrainOrderItem.Rid"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
        },
    )
    train_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
            "length": 4,
            "pattern": r"[0-9][A-Z][0-9][0-9]",
        },
    )

    @dataclass
    class Rid:
        """
        :ivar value:
        :ivar wta: Working time of arrival.
        :ivar wtd: Working time of departure.
        :ivar wtp: Working time of pass.
        :ivar pta: Public time of arrival.
        :ivar ptd: Public time of departure.
        """

        value: str = field(
            default="",
            metadata={
                "required": True,
                "max_length": 16,
            },
        )
        wta: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
            },
        )
        wtd: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
            },
        )
        wtp: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
            },
        )
        pta: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
            },
        )
        ptd: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
            },
        )


@dataclass
class TrainOrderData:
    """
    Defines the sequence of trains making up the train order.

    :ivar first: The first train in the train order.
    :ivar second: The second train in the train order.
    :ivar third: The third train in the train order.
    """

    first: Optional[TrainOrderItem] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
            "required": True,
        },
    )
    second: Optional[TrainOrderItem] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
        },
    )
    third: Optional[TrainOrderItem] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
        },
    )


@dataclass
class TrainOrder:
    """
    Defines the expected Train order at a platform.

    :ivar set:
    :ivar clear: Clear the current train order
    :ivar tiploc: The tiploc where the train order applies
    :ivar crs: The CRS code of the station where the train order applies
    :ivar platform: The platform number where the train order applies
    """

    set: Optional[TrainOrderData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
        },
    )
    clear: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainOrder/v1",
        },
    )
    tiploc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    crs: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 3,
        },
    )
    platform: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 3,
        },
    )
