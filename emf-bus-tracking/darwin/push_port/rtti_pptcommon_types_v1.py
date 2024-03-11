from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/CommonTypes/v1"


@dataclass
class DisruptionReasonType:
    """
    Type used to represent a cancellation or late running reason.

    :ivar value:
    :ivar tiploc: Optional TIPLOC where the reason refers to, e.g.
        "signalling failure at Cheadle Hulme".
    :ivar near: If true, the tiploc attribute should be interpreted as
        "near", e.g. "signalling failure near Cheadle Hulme".
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    tiploc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 7,
        },
    )
    near: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
