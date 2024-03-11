from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from xsdata.models.datatype import XmlDate

from darwin.push_port.rtti_pptcommon_types_v1 import DisruptionReasonType

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3"


class PlatformDataPlatsrc(Enum):
    P = "P"
    A = "A"
    M = "M"


@dataclass
class TstimeData:
    """
    Type describing time-based forecast attributes for a TS arrival/departure/pass.

    :ivar et: Estimated Time. For locations that are public stops, this
        will be based on the "public schedule". For operational stops
        and passing locations, it will be based on the "working
        schedule". It is only published where there is a corresponding
        "activity" for the service.
    :ivar wet: The estimated time based on the "working schedule". This
        will only be set for public stops when (i) it also differs from
        the estimated time based on the "public schedule", or (ii) where
        there is an operational "activity" but no public "activity".
    :ivar at: Actual Time
    :ivar at_removed: If true, indicates that an actual time ("at")
        value has just been removed and replaced by an estimated time
        ("et"). Note that this attribute will only be set to "true"
        once, when the actual time is removed, and will not be set in
        any snapshot.
    :ivar at_class: The class of the actual time.
    :ivar etmin: The manually applied lower limit that has been applied
        to the estimated time at this location. The estimated time will
        not be set lower than this value, but may be set higher.
    :ivar et_unknown: Indicates that an unknown delay forecast has been
        set for the estimated time at this location. Note that this
        value indicates where a manual unknown delay forecast has been
        set, whereas it is the "delayed" attribute that indicates that
        the actual forecast is "unknown delay".
    :ivar delayed: Indicates that this estimated time is a forecast of
        "unknown delay". Displayed  as "Delayed" in LDB. Note that this
        value indicates that this forecast is "unknown delay", whereas
        it is the "etUnknown" attribute that indicates where the manual
        unknown delay forecast has been set.
    :ivar src: The source of the forecast or actual time.
    :ivar src_inst: The RTTI CIS code of the CIS instance if the src is
        a CIS.
    """

    class Meta:
        name = "TSTimeData"

    et: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
        },
    )
    wet: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
        },
    )
    at: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
        },
    )
    at_removed: bool = field(
        default=False,
        metadata={
            "name": "atRemoved",
            "type": "Attribute",
        },
    )
    at_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "atClass",
            "type": "Attribute",
        },
    )
    etmin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([0-1][0-9]|2[0-3]):[0-5][0-9]",
        },
    )
    et_unknown: bool = field(
        default=False,
        metadata={
            "name": "etUnknown",
            "type": "Attribute",
        },
    )
    delayed: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
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
class PlatformData:
    """
    Platform number with associated flags.

    :ivar value:
    :ivar platsup: Platform number is suppressed and should not be
        displayed.
    :ivar cis_platsup: Whether a CIS, or Darwin Workstation, has set
        platform suppression at this location.
    :ivar platsrc: The source of the platfom number. P = Planned, A =
        Automatic, M = Manual.
    :ivar conf: True if the platform number is confirmed.
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 3,
        },
    )
    platsup: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    cis_platsup: bool = field(
        default=False,
        metadata={
            "name": "cisPlatsup",
            "type": "Attribute",
        },
    )
    platsrc: PlatformDataPlatsrc = field(
        default=PlatformDataPlatsrc.P,
        metadata={
            "type": "Attribute",
            "length": 1,
        },
    )
    conf: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Tslocation:
    """
    Forecast data for an individual location in the service's schedule.

    :ivar arr: Forecast data for the arrival at this location
    :ivar dep: Forecast data for the departure at this location
    :ivar pass_value: Forecast data for the pass of this location
    :ivar plat: Current platform number
    :ivar suppr: The service is suppressed at this location.
    :ivar length: The length of the service at this location on
        departure (or arrival at destination). The default value of zero
        indicates that the length is unknown.
    :ivar detach_front: Indicates from which end of the train stock will
        be detached. The value is set to “true” if stock will be
        detached from the front of the train at this location. It will
        be set at each location where stock will be detached from the
        front. Darwin will not validate that a stock detachment activity
        code applies at this location.
    :ivar tpl: TIPLOC
    :ivar wta: Working time of arrival.
    :ivar wtd: Working time of departure.
    :ivar wtp: Working time of pass.
    :ivar pta: Public time of arrival.
    :ivar ptd: Public time of departure.
    """

    class Meta:
        name = "TSLocation"

    arr: Optional[TstimeData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    dep: Optional[TstimeData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    pass_value: Optional[TstimeData] = field(
        default=None,
        metadata={
            "name": "pass",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    plat: Optional[PlatformData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    suppr: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    length: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
            "max_inclusive": 99,
        },
    )
    detach_front: Optional[bool] = field(
        default=None,
        metadata={
            "name": "detachFront",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
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
class Ts:
    """Train Status.

    Update to the "real time" forecast data for a service.

    :ivar late_reason: Late running reason for this service. The reason
        applies to all locations of this service.
    :ivar location: Update of forecast data for an individual location
        in the service's schedule
    :ivar rid: RTTI unique Train Identifier
    :ivar uid: Train UID
    :ivar ssd: Scheduled Start Date
    :ivar is_reverse_formation: Indicates whether a train that divides
        is working with portions in reverse to their normal formation.
        The value applies to the whole train. Darwin will not validate
        that a divide association actually exists for this service.
    """

    class Meta:
        name = "TS"

    late_reason: Optional[DisruptionReasonType] = field(
        default=None,
        metadata={
            "name": "LateReason",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
        },
    )
    location: List[Tslocation] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3",
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
    ssd: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    is_reverse_formation: bool = field(
        default=False,
        metadata={
            "name": "isReverseFormation",
            "type": "Attribute",
        },
    )
