from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "http://thalesgroup.com/RTTI/PushPortRequestTD/root_1"


@dataclass
class RequestTd:
    """
    Request to filter TD-related push port data by the supplied list of TD Area
    codes.
    """

    class Meta:
        name = "RequestTD"
        namespace = "http://thalesgroup.com/RTTI/PushPortRequestTD/root_1"

    td: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "pattern": r"\S{2}",
        },
    )
