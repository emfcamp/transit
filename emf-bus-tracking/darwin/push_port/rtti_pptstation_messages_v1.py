from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1"


class MsgCategoryType(Enum):
    """
    The category of operator message.
    """

    TRAIN = "Train"
    STATION = "Station"
    CONNECTIONS = "Connections"
    SYSTEM = "System"
    MISC = "Misc"
    PRIOR_TRAINS = "PriorTrains"
    PRIOR_OTHER = "PriorOther"


class MsgSeverityType(Enum):
    """
    The severity of operator message.
    """

    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"


@dataclass
class A:
    """
    Defines an HTML anchor.
    """

    class Meta:
        name = "a"
        namespace = (
            "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1"
        )

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class P:
    """
    Defines an HTML paragraph.
    """

    class Meta:
        name = "p"
        namespace = (
            "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1"
        )

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": A,
                },
            ),
        },
    )


@dataclass
class StationMessage:
    """
    Darwin Workstation Station Message.

    :ivar station: The Stations the message is being applied to
    :ivar msg: The content of the message
    :ivar id:
    :ivar cat: The category of message
    :ivar sev: The severity of the message
    :ivar suppress: Whether the train running information is suppressed
        to the public
    """

    station: List["StationMessage.Station"] = field(
        default_factory=list,
        metadata={
            "name": "Station",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1",
        },
    )
    msg: Optional["StationMessage.Msg"] = field(
        default=None,
        metadata={
            "name": "Msg",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1",
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    cat: Optional[MsgCategoryType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sev: Optional[MsgSeverityType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    suppress: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Station:
        crs: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
                "length": 3,
            },
        )

    @dataclass
    class Msg:
        content: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
                "choices": (
                    {
                        "name": "p",
                        "type": P,
                        "namespace": "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1",
                    },
                    {
                        "name": "a",
                        "type": A,
                        "namespace": "http://www.thalesgroup.com/rtti/PushPort/StationMessages/v1",
                    },
                ),
            },
        )
