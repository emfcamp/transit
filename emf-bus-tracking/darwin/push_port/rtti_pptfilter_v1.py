from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "http://thalesgroup.com/RTTI/PushPortFilter/root_1"


@dataclass
class FilterTiplocs:
    """
    Request to filter push port data by the supplied list of TIPLOCs.
    """

    class Meta:
        namespace = "http://thalesgroup.com/RTTI/PushPortFilter/root_1"

    tiploc: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "pattern": r"\S{1,7}",
        },
    )
