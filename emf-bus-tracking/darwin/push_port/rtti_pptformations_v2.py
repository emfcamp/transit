from dataclasses import dataclass, field
from typing import List, Optional

from darwin.push_port.rtti_pptcommon_types_v4 import ToiletAvailabilityType

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/Formations/v2"


@dataclass
class CoachData:
    """
    Data for an individual coach in a formation.

    :ivar toilet: The availability of a toilet in this coach. E.g.
        "Unknown", "None" , "Standard" or "Accessible". Note that other
        values may be supplied in the future without a schema change. If
        no toilet availability is supplied then it should be assumed to
        be "Unknown".
    :ivar coach_number: The number/identifier for this coach, e.g. "A".
    :ivar coach_class: The class of the coach, e.g. "First" or
        "Standard".
    """

    toilet: Optional[ToiletAvailabilityType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v2",
        },
    )
    coach_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "coachNumber",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 2,
        },
    )
    coach_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "coachClass",
            "type": "Attribute",
        },
    )


@dataclass
class CoachList:
    """
    A list of coach data for a formation.

    :ivar coach: An individual coach in a formation.
    """

    coach: List[CoachData] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v2",
            "min_occurs": 1,
        },
    )


@dataclass
class Formation:
    """
    Type describing a Train Formation for a Schedule.

    :ivar coaches: A list of coaches in this formation.
    :ivar fid: The unique identifier of this formation data.
    :ivar src: The source of the formation data.
    :ivar src_inst: The RTTI instance ID of the src (if any).
    """

    coaches: Optional[CoachList] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v2",
            "required": True,
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 20,
        },
    )
    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    src_inst: Optional[str] = field(
        default=None,
        metadata={
            "name": "srcInst",
            "type": "Attribute",
            "length": 4,
        },
    )


@dataclass
class ScheduleFormations:
    """
    Type describing all of the Train Formations set for a Schedule.

    :ivar formation: An individual formation for all or part of the
        service.
    :ivar rid: RTTI unique Train Identifier
    """

    formation: List[Formation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v2",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 16,
        },
    )
