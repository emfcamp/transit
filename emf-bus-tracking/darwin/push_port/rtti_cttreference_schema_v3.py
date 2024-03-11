from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/XmlRefData/v3"


@dataclass
class Cissource:
    """
    Defines the mapping between 4 letter CIS codes and the CIS name.

    :ivar code: This is the 4 letter CIS code
    :ivar name: The CIS name
    """

    class Meta:
        name = "CISSource"
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 4,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 0,
            "max_length": 30,
        },
    )


@dataclass
class LocationRef:
    """
    Defines a location.

    :ivar tpl: TIPLOC code
    :ivar crs: CRS code
    :ivar toc: Train Operating Company that manages the station (may be
        non-TOC code, e.g. Network Rail).
    :ivar locname: English name of location
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 7,
        },
    )
    crs: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "length": 3,
        },
    )
    toc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "length": 2,
        },
    )
    locname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 30,
            "white_space": "preserve",
        },
    )


@dataclass
class Reason:
    """
    Defines a mapping bewteen a reason code and the corresponding text.
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    code: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    reasontext: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        },
    )


@dataclass
class TocRef:
    """
    Defines a mapping between a TOC and a displayable name.

    :ivar toc: The TOC code
    :ivar tocname: The name of the TOC
    :ivar url:
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    toc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 2,
        },
    )
    tocname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 0,
            "max_length": 256,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 0,
            "max_length": 512,
        },
    )


@dataclass
class Via:
    """
    Defines the locations a journey must be viewed from, go to and pass through for
    the corresponding via text to be displayed.

    :ivar at: This is the station for which the via is defined
    :ivar dest: The destination of the journey must match this before
        the via text is valid
    :ivar loc1: The journey must call at this station before the via
        text is valid.
    :ivar loc2: The journey must call at this station (after the call at
        loc1) before the via text is valid.
    :ivar viatext: The via text to display if a journey matches the
        previous attributes
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    at: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 3,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 7,
        },
    )
    loc1: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 7,
        },
    )
    loc2: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 7,
        },
    )
    viatext: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        },
    )


@dataclass
class PportTimetableRef:
    """
    Push Port Timetable Reference Schema.
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/XmlRefData/v3"

    location_ref: List[LocationRef] = field(
        default_factory=list,
        metadata={
            "name": "LocationRef",
            "type": "Element",
        },
    )
    toc_ref: List[TocRef] = field(
        default_factory=list,
        metadata={
            "name": "TocRef",
            "type": "Element",
        },
    )
    late_running_reasons: Optional["PportTimetableRef.LateRunningReasons"] = (
        field(
            default=None,
            metadata={
                "name": "LateRunningReasons",
                "type": "Element",
            },
        )
    )
    cancellation_reasons: Optional["PportTimetableRef.CancellationReasons"] = (
        field(
            default=None,
            metadata={
                "name": "CancellationReasons",
                "type": "Element",
            },
        )
    )
    via: List[Via] = field(
        default_factory=list,
        metadata={
            "name": "Via",
            "type": "Element",
        },
    )
    cissource: List[Cissource] = field(
        default_factory=list,
        metadata={
            "name": "CISSource",
            "type": "Element",
        },
    )
    timetable_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "timetableId",
            "type": "Attribute",
            "required": True,
            "length": 14,
        },
    )

    @dataclass
    class LateRunningReasons:
        reason: List[Reason] = field(
            default_factory=list,
            metadata={
                "name": "Reason",
                "type": "Element",
                "min_occurs": 1,
            },
        )

    @dataclass
    class CancellationReasons:
        reason: List[Reason] = field(
            default_factory=list,
            metadata={
                "name": "Reason",
                "type": "Element",
                "min_occurs": 1,
            },
        )
