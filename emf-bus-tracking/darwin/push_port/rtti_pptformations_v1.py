from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/Formations/v1"


@dataclass
class CoachData:
    """
    Data for an individual coach in a formation.

    :ivar coach_number: The number/identifier for this coach, e.g. "A".
    :ivar coach_class: The class of the coach, e.g. "First" or
        "Standard".
    """

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
class CoachLoadingData:
    """
    Type describing the loading data for an identified coach.

    :ivar value:
    :ivar coach_number: The number/identifier for this coach, e.g. "A".
    :ivar src: The source of the loading data.
    :ivar src_inst: The RTTI instance ID of the src (if any).
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
            "max_inclusive": 100,
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
class CoachList:
    """
    A list of coach data for a formation.

    :ivar coach: An individual coach in a formation.
    """

    coach: List[CoachData] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v1",
            "min_occurs": 1,
        },
    )


@dataclass
class Loading:
    """
    Loading data for an individual location in a schedule linked to a formation.

    :ivar loading: Loading data for an individual coach in the
        formation. If no loading data is provided for a coach in the
        formation then it should be assumed to have been cleared.
    :ivar fid: The unique identifier of the formation data.
    :ivar rid: RTTI unique Train ID
    :ivar tpl: TIPLOC where the loading data applies.
    :ivar wta: Working time of arrival.
    :ivar wtd: Working time of departure.
    :ivar wtp: Working time of pass.
    :ivar pta: Public time of arrival.
    :ivar ptd: Public time of departure.
    """

    loading: List[CoachLoadingData] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v1",
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
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 16,
        },
    )
    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
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
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v1",
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
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Formations/v1",
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
