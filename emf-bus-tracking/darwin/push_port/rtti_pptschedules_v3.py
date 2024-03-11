from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDate

from darwin.push_port.rtti_pptcommon_types_v1 import DisruptionReasonType

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3"


@dataclass
class Dt:
    """
    Defines a Passenger Destination Calling point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar pta: Public Scheduled Time of Arrival
    :ivar ptd: Public Scheduled Time of Departure
    :ivar avg_loading: Average Loading of the train as a whole at this
        Calling Point. This is a fixed value that is based on long-term
        averages and does not vary according to real-time actual
        loading.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    :ivar rdelay: A delay value that is implied by a change to the
        service's route. This value has been added to the forecast
        lateness of the service at the previous schedule location when
        calculating the expected lateness of arrival at this location.
    """

    class Meta:
        name = "DT"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
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
    avg_loading: Optional[int] = field(
        default=None,
        metadata={
            "name": "avgLoading",
            "type": "Attribute",
            "max_inclusive": 100,
        },
    )
    wta: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
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
    rdelay: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Ip:
    """
    Defines aPassenger Intermediate Calling Point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar pta: Public Scheduled Time of Arrival
    :ivar ptd: Public Scheduled Time of Departure
    :ivar avg_loading: Average Loading of the train as a whole at this
        Calling Point. This is a fixed value that is based on long-term
        averages and does not vary according to real-time actual
        loading.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    :ivar rdelay: A delay value that is implied by a change to the
        service's route. This value has been added to the forecast
        lateness of the service at the previous schedule location when
        calculating the expected lateness of arrival at this location.
    :ivar fd: TIPLOC of False Destination to be used at this location
    """

    class Meta:
        name = "IP"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
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
    avg_loading: Optional[int] = field(
        default=None,
        metadata={
            "name": "avgLoading",
            "type": "Attribute",
            "max_inclusive": 100,
        },
    )
    wta: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    wtd: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    rdelay: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    fd: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 7,
        },
    )


@dataclass
class Opdt:
    """
    Defines an Operational Destination Calling point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    :ivar rdelay: A delay value that is implied by a change to the
        service's route. This value has been added to the forecast
        lateness of the service at the previous schedule location when
        calculating the expected lateness of arrival at this location.
    """

    class Meta:
        name = "OPDT"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
        },
    )
    wta: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
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
    rdelay: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Opip:
    """
    Defines an Operational Intermediate Calling Point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    :ivar rdelay: A delay value that is implied by a change to the
        service's route. This value has been added to the forecast
        lateness of the service at the previous schedule location when
        calculating the expected lateness of arrival at this location.
    """

    class Meta:
        name = "OPIP"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
        },
    )
    wta: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    wtd: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    rdelay: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Opor:
    """
    Defines an Operational Origin Calling Point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    """

    class Meta:
        name = "OPOR"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
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
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )


@dataclass
class Or:
    """
    Defines a Passenger Origin Calling Point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar pta: Public Scheduled Time of Arrival
    :ivar ptd: Public Scheduled Time of Departure
    :ivar avg_loading: Average Loading of the train as a whole at this
        Calling Point. This is a fixed value that is based on long-term
        averages and does not vary according to real-time actual
        loading.
    :ivar wta: Working Scheduled Time of Arrival
    :ivar wtd: Working Scheduled Time of Departure
    :ivar fd: TIPLOC of False Destination to be used at this location
    """

    class Meta:
        name = "OR"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
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
    avg_loading: Optional[int] = field(
        default=None,
        metadata={
            "name": "avgLoading",
            "type": "Attribute",
            "max_inclusive": 100,
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
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    fd: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 7,
        },
    )


@dataclass
class Pp:
    """
    Defines an Intermediate Passing Point.

    :ivar tpl: TIPLOC
    :ivar act: Current Activity Codes
    :ivar plan_act: Planned Activity Codes (if different to current
        activities)
    :ivar can: Cancelled
    :ivar fid: The unique identifier of the formation data that has been
        set at this location. If not present, the formation is unknown
        at this location.
    :ivar wtp: Working Scheduled Time of Passing
    :ivar rdelay: A delay value that is implied by a change to the
        service's route. This value has been added to the forecast
        lateness of the service at the previous schedule location when
        calculating the expected lateness of passing this location.
    """

    class Meta:
        name = "PP"

    tpl: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 7,
        },
    )
    act: str = field(
        default="  ",
        metadata={
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    plan_act: Optional[str] = field(
        default=None,
        metadata={
            "name": "planAct",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 12,
            "white_space": "preserve",
            "pattern": r"([A-Z0-9\- ][A-Z0-9\- ]){1,6}",
        },
    )
    can: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    fid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
        },
    )
    wtp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
        },
    )
    rdelay: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Schedule:
    """
    Train Schedule.

    :ivar or_value:
    :ivar opor:
    :ivar ip:
    :ivar opip:
    :ivar pp:
    :ivar dt:
    :ivar opdt:
    :ivar cancel_reason:
    :ivar rid: RTTI unique Train ID
    :ivar uid: Train UID
    :ivar train_id: Train ID (Headcode)
    :ivar rsid: Retail Service Identifier. Note that this may be either
        a full 8-character "portion identifier", or a base 6-character
        identifier, according to the available information provided to
        Darwin.
    :ivar ssd: Scheduled Start Date
    :ivar toc: ATOC Code
    :ivar status: Type of service, i.e. Train/Bus/Ship.
    :ivar train_cat: Category of service.
    :ivar is_passenger_svc: True if Darwin classifies the train category
        as a passenger service.
    :ivar is_active: Indicates if this service is active in Darwin. Note
        that schedules should be assumed to be inactive until a message
        is received to indicate otherwise.
    :ivar deleted: Service has been deleted and should not be
        used/displayed.
    :ivar is_charter: Indicates if this service is a charter service.
    """

    or_value: List[Or] = field(
        default_factory=list,
        metadata={
            "name": "OR",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    opor: List[Opor] = field(
        default_factory=list,
        metadata={
            "name": "OPOR",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    ip: List[Ip] = field(
        default_factory=list,
        metadata={
            "name": "IP",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    opip: List[Opip] = field(
        default_factory=list,
        metadata={
            "name": "OPIP",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    pp: List[Pp] = field(
        default_factory=list,
        metadata={
            "name": "PP",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    dt: List[Dt] = field(
        default_factory=list,
        metadata={
            "name": "DT",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    opdt: List[Opdt] = field(
        default_factory=list,
        metadata={
            "name": "OPDT",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
            "min_occurs": 2,
        },
    )
    cancel_reason: Optional[DisruptionReasonType] = field(
        default=None,
        metadata={
            "name": "cancelReason",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Schedules/v3",
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
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 6,
        },
    )
    train_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainId",
            "type": "Attribute",
            "required": True,
            "length": 4,
            "pattern": r"[0-9][A-Z][0-9][0-9]",
        },
    )
    rsid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 6,
            "max_length": 8,
        },
    )
    ssd: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    toc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 2,
        },
    )
    status: str = field(
        default="P",
        metadata={
            "type": "Attribute",
            "length": 1,
            "pattern": r"[BFPST12345]",
        },
    )
    train_cat: str = field(
        default="OO",
        metadata={
            "name": "trainCat",
            "type": "Attribute",
            "min_length": 0,
            "max_length": 2,
        },
    )
    is_passenger_svc: bool = field(
        default=True,
        metadata={
            "name": "isPassengerSvc",
            "type": "Attribute",
        },
    )
    is_active: bool = field(
        default=True,
        metadata={
            "name": "isActive",
            "type": "Attribute",
        },
    )
    deleted: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    is_charter: bool = field(
        default=False,
        metadata={
            "name": "isCharter",
            "type": "Attribute",
        },
    )
