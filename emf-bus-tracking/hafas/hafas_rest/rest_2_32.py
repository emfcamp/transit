from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime, XmlDuration

__NAMESPACE__ = "http://hacon.de/hafas/proxy/hafas-proxy"


class ApplyToType(Enum):
    """
    :cvar F: First mile
    :cvar B: Last mile
    :cvar FB: First and last mile
    :cvar T: Total
    :cvar FBT: First mile, last mile and total
    """

    F = "F"
    B = "B"
    FB = "FB"
    T = "T"
    FBT = "FBT"


class ArrivalType(Enum):
    ST = "ST"
    ADR = "ADR"
    POI = "POI"
    CRD = "CRD"
    MCP = "MCP"
    HL = "HL"


class AvoidStatusType(Enum):
    NCAVM = "NCAVM"
    NCAVO = "NCAVO"
    NPAVM = "NPAVM"
    NPAVO = "NPAVO"


@dataclass
class BooleanKvtype:
    class Meta:
        name = "BooleanKVType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class CalculationType(Enum):
    """
    Indicates whether the connection originated from the initial search using the
    original parameters, or from a retried search with changed parameters that was
    performed after the initial search failed.

    :cvar INITIAL: The connection was computed during the initial
        request execution with the original parameters.
    :cvar RETRY_SHARP: The connection was found using a sharp search
        that was performed after an unsharp search failed.
    :cvar RETRY_UNSHARP: The connection was found using an unsharp
        search that was performed after a sharp search failed.
    :cvar RETRY_DOUBLE_RADIUS: The connection was found only after the
        original GIS radiuses for front/back were doubled at least once.
    :cvar RETRY_UNSHARP_NEW_RADIUS: The connection was found using an
        additional unsharp search that was performed with an increased
        footpath distance.
    :cvar RETRY_PRESELECTION_NEW_RADIUS: The connection was found using
        extended gis radii after the initial trip search from/to an
        address/poi/coordinate either found no suitable station within
        the originally specified radii, or was not able to find a GIS
        route to any of them.
    """

    INITIAL = "INITIAL"
    RETRY_SHARP = "RETRY_SHARP"
    RETRY_UNSHARP = "RETRY_UNSHARP"
    RETRY_DOUBLE_RADIUS = "RETRY_DOUBLE_RADIUS"
    RETRY_UNSHARP_NEW_RADIUS = "RETRY_UNSHARP_NEW_RADIUS"
    RETRY_PRESELECTION_NEW_RADIUS = "RETRY_PRESELECTION_NEW_RADIUS"


class ConnectionReliabilityValueType(Enum):
    """
    :cvar GUARANTEED: Guaranteed to get the user from A to B in time
        within the scope
    :cvar HIGH: Likely to get the user from A to B in time within the
        scope
    :cvar LOW: Unlikely to get the user from A to B in time within the
        scope
    :cvar ABORTIVE: Definitely not going to get the user from A to B in
        time within the scope
    :cvar UNDEF: No information
    """

    GUARANTEED = "GUARANTEED"
    HIGH = "HIGH"
    LOW = "LOW"
    ABORTIVE = "ABORTIVE"
    UNDEF = "UNDEF"


class CoordLocationType(Enum):
    ADR = "ADR"
    POI = "POI"
    CRD = "CRD"
    MCP = "MCP"
    HL = "HL"


class CoordType(Enum):
    WGS84 = "WGS84"
    PLANAR = "PLANAR"
    HAFASGEO = "HAFASGEO"


@dataclass
class Coordinate:
    """
    Coordinate.

    :ivar lon: Longitude
    :ivar lat: Latitude
    :ivar alt: Altitude
    """

    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class DateTimeIntervalType:
    """
    :ivar s_time: Start time of the interval in format hh:mm[:ss]
    :ivar s_date: Start date of the interval in format YYYY-MM-DD.
    :ivar e_time: End time of the interval in format hh:mm[:ss]
    :ivar e_date: End date of the interval in format YYYY-MM-DD.
    """

    s_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "sTime",
            "type": "Attribute",
        },
    )
    s_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDate",
            "type": "Attribute",
        },
    )
    e_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "eTime",
            "type": "Attribute",
        },
    )
    e_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "eDate",
            "type": "Attribute",
        },
    )


class DepartureType(Enum):
    ST = "ST"
    ADR = "ADR"
    POI = "POI"
    CRD = "CRD"
    MCP = "MCP"
    HL = "HL"


@dataclass
class Direction:
    """Direction information.

    This is usually the last stop of the journey.

    :ivar value:
    :ivar flag: Direction flag of the journey.
    :ivar route_idx_from: Defines the first stop/station where this type
        is valid. See the Stops list for details of the stop/station.
    :ivar route_idx_to: Defines the last stop/station where this type is
        valid. See the Stops list for details of the stop/station.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    flag: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx_from: int = field(
        default=-1,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: int = field(
        default=-1,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )


@dataclass
class EcoType:
    """
    :ivar co2: CO2 emission in kg
    :ivar co2f: CO2 emission, in operation only in kg
    :ivar part: Particulate matter emission (25). This value includes
        possible particulate matter emissions occurring when generating
        the energy used for the vehicle during the trip. For example,
        electric cars will still have a non-zero particulate matter
        emission although the vehicle doesn't emit anything but the
        electric energy used by the vehicle might be generated from coal
        power plants and those created emissions during energy
        generation. Unit is g.
    :ivar part10: Particulate matter emission (10). This value includes
        possible particulate matter emissions occurring when generating
        the energy used for the vehicle during the trip. For example,
        electric cars will still have a non-zero particulate matter
        emission although the vehicle doesn't emit anything but the
        electric energy used by the vehicle might be generated from coal
        power plants and those created emissions during energy
        generation. Unit is g.
    :ivar part_v: Particulate matter emission per vehicle (25). This
        value contains only the emission generated by the vehicle on
        this trip. Emissions which were generated during generation of
        the energy used by the vehicle are ignored by this value. Unit
        is g.
    :ivar nmhc: NMHC emission in g
    :ivar nox: NOX emission in g
    :ivar prime: PRIME emission, calculated in l petrol
    :ivar primef: PRIMEF emission, in operation only, calculated in l
        petrol
    :ivar so2: SO2 emission in g
    :ivar ubp: environmental impact points 06
    :ivar dist: Distance the emitting carrier is used in meter.
    :ivar type_value: Type of emitting carrier. Values are PUT: public
        transport, PFT: public flight transport, PRT: private transport,
        BEE: Estimation - Emission computed based on a reference value
        and beeline between start and destination
    :ivar nmvoc: NMVOC emission in g
    :ivar ubp13: UBP measurement based on 2013 standard
    :ivar co2el: CO2 emission in g for electric vehicles
    :ivar prime_energy: PRIME emission, in operation only, calculated in
        l petrol
    :ivar rating: Rating of connection regarding its ecological values
    """

    co2: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    co2f: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    part: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    part10: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    part_v: Optional[float] = field(
        default=None,
        metadata={
            "name": "partV",
            "type": "Attribute",
        },
    )
    nmhc: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nox: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    prime: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    primef: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    so2: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ubp: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dist: int = field(
        default=-1,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: str = field(
        default="PUT",
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    nmvoc: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ubp13: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    co2el: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    prime_energy: Optional[float] = field(
        default=None,
        metadata={
            "name": "primeEnergy",
            "type": "Attribute",
        },
    )
    rating: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class GeoDataTypeType(Enum):
    """
    :cvar GEO_JSON: Base64 encoded GeoJson text.
    """

    GEO_JSON = "GeoJSON"


class GeoFeatureTypeType(Enum):
    """
    :cvar TRAFFIC: Traffic-related GeoFeature.
    :cvar SERVICE_AREA: Service area of some provider.
    :cvar BICYCLE_PATH: Path of a bicycle route.
    :cvar STATION_AREA: Station area of some provider.
    """

    TRAFFIC = "TRAFFIC"
    SERVICE_AREA = "SERVICE_AREA"
    BICYCLE_PATH = "BICYCLE_PATH"
    STATION_AREA = "STATION_AREA"


@dataclass
class GisEdgeType:
    """
    :ivar edge_id: The ID for this edge.
    :ivar graph_id: The ID of the graph, that this edge belongs to.
    """

    edge_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "edgeId",
            "type": "Attribute",
        },
    )
    graph_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "graphId",
            "type": "Attribute",
        },
    )


class GisProfileType(Enum):
    """
    :cvar F: Foot
    :cvar B: Bike
    :cvar P: Car to Parking / Park'n'Ride
    :cvar K: Car / Kiss'n'Ride
    :cvar T: Taxi
    :cvar TE: Taxistand
    """

    F = "F"
    B = "B"
    P = "P"
    K = "K"
    T = "T"
    TE = "TE"


@dataclass
class GisRef:
    """
    Reference to individual route of this leg.

    :ivar ref: Contains a reference to call the ReST interface for GIS
        route for this leg.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class GisRouteManoeuvre(Enum):
    """
    :cvar NO: Not set
    :cvar FR: From
    :cvar TO: To
    :cvar ON: On
    :cvar LE: Left
    :cvar RI: Right
    :cvar KL: Keep left
    :cvar KR: Keep right
    :cvar HL: Half left
    :cvar HR: Half right
    :cvar KHL: Keep half left
    :cvar KHR: Keep half right
    :cvar SL: Sharp left
    :cvar SR: Sharp right
    :cvar KSL: Keep sharp left
    :cvar KSR: Keep sharp right
    :cvar ST: Straight
    :cvar UT: U-Turn
    :cvar EN: Enter
    :cvar LV: Leave
    :cvar ER: Enter roundabout
    :cvar SIR: Stay in roundabout
    :cvar LR: Leave roundabout
    :cvar EF: Enter ferry
    :cvar LF: Leave ferry
    :cvar CH: Change highway
    :cvar CIF: Check-in ferry
    :cvar COF: Check-out ferry
    :cvar EL: Elevator
    :cvar ELD: Elevator down
    :cvar ELU: Elevator up
    :cvar ES: Escalator
    :cvar ESD: Escalator down
    :cvar ESU: Escalator up
    :cvar STA: Stairs
    :cvar STD: Stairs down
    :cvar STU: Stairs up
    """

    NO = "NO"
    FR = "FR"
    TO = "TO"
    ON = "ON"
    LE = "LE"
    RI = "RI"
    KL = "KL"
    KR = "KR"
    HL = "HL"
    HR = "HR"
    KHL = "KHL"
    KHR = "KHR"
    SL = "SL"
    SR = "SR"
    KSL = "KSL"
    KSR = "KSR"
    ST = "ST"
    UT = "UT"
    EN = "EN"
    LV = "LV"
    ER = "ER"
    SIR = "SIR"
    LR = "LR"
    EF = "EF"
    LF = "LF"
    CH = "CH"
    CIF = "CIF"
    COF = "COF"
    EL = "EL"
    ELD = "ELD"
    ELU = "ELU"
    ES = "ES"
    ESD = "ESD"
    ESU = "ESU"
    STA = "STA"
    STD = "STD"
    STU = "STU"


class GisRouteOrientation(Enum):
    """
    :cvar U: Unknown
    :cvar N: North
    :cvar S: South
    :cvar E: East
    :cvar W: West
    :cvar NE: Northeast
    :cvar SE: Southeast
    :cvar NW: Northwest
    :cvar SW: Southwest
    """

    U = "U"
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NE = "NE"
    SE = "SE"
    NW = "NW"
    SW = "SW"


class GisRouteRoadType(Enum):
    """
    Type of road.

    :cvar U: Unknown
    :cvar M: Motorway
    :cvar H: Highway
    :cvar T: Trunk road
    :cvar T4_L: Trunk road with four lanes
    :cvar T2_L: Trunk road with two lanes
    :cvar TR: Country road
    :cvar NT: County road
    :cvar CT: City road
    :cvar R: Residential road
    :cvar B: Blocked road
    :cvar CW: Combined cycle and walkway
    :cvar C: Cycleway
    :cvar W: Walkway
    :cvar F: Ferry
    """

    U = "U"
    M = "M"
    H = "H"
    T = "T"
    T4_L = "T4L"
    T2_L = "T2L"
    TR = "TR"
    NT = "NT"
    CT = "CT"
    R = "R"
    B = "B"
    CW = "CW"
    C = "C"
    W = "W"
    F = "F"


class IconShapeType(Enum):
    """
    :cvar U: Unknown shape
    :cvar R: Rectangle
    :cvar C: Circle
    :cvar RES: Use shape described in @shapeRes
    """

    U = "U"
    R = "R"
    C = "C"
    RES = "RES"


class IconStyleType(Enum):
    """
    :cvar U: Unknown text style
    :cvar N: Normal
    :cvar B: Bold
    :cvar I: Italic
    :cvar BI: Bold Italic
    """

    U = "U"
    N = "N"
    B = "B"
    I = "I"
    BI = "BI"


@dataclass
class JourneyDetailRef:
    """
    Reference to journey details of this leg.

    :ivar ref: Contains an internal journey id which must use for a
        subsequent journey detail request.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 512,
        },
    )


class JourneyPathItemStateType(Enum):
    """
    :cvar U: Undefined
    :cvar B: Journey is before relevant segement.
    :cvar O: Journey is on relevant segement.
    :cvar A: Journey is after relevant segement.
    """

    U = "U"
    B = "B"
    O = "O"
    A = "A"


class JourneyStatusType(Enum):
    """
    Contains the status of the journey.

    :cvar P: Planned: A planned journey. This is also the default value.
    :cvar R: Replacement: The journey was added as a replacement for a
        planned journey.
    :cvar A: Additional: The journey is an additional journey to the
        planned journeys.
    :cvar S: Special: This is a special journey. The exact definition
        which journeys are considered special up to the customer.
    """

    P = "P"
    R = "R"
    A = "A"
    S = "S"


class JourneyStatusValue(Enum):
    """
    :cvar P: Planned: A planned journey. This is also the default value.
    :cvar R: Replacement: The journey was added as a replacement for a
        planned journey.
    :cvar A: Additional: The journey is an additional journey to the
        planned journeys.
    :cvar S: Special: This is a special journey. The exact definition
        which journeys are considered special up to the customer.
    """

    P = "P"
    R = "R"
    A = "A"
    S = "S"


@dataclass
class Kvtype:
    class Meta:
        name = "KVType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 64,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 128,
        },
    )


class LocationPreselectionModeType(Enum):
    """
    :cvar ESTIMATE: Only perform preselection and do not perform any 1:n
        routing - the resulting connections will be filled with beeline
        distance.
    :cvar ROUTE: Perform preselection and perform 1:n routing for all
        modes - the resulting connections will be filled with routed
        distance and duration.
    """

    ESTIMATE = "ESTIMATE"
    ROUTE = "ROUTE"


class LocationPreselectionStrategyType(Enum):
    """
    :cvar ONE_TO_N_SELECTION: Indicates that we are searching locations
        for 1:n.
    :cvar N_TO_ONE_SELECTION: Indicates that we are searching locations
        for n:1.
    """

    ONE_TO_N_SELECTION = "ONE_TO_N_SELECTION"
    N_TO_ONE_SELECTION = "N_TO_ONE_SELECTION"


class LocationType(Enum):
    ADR = "ADR"
    POI = "POI"
    CRD = "CRD"
    MCP = "MCP"
    HL = "HL"


class MapLayerTypeProjection(Enum):
    """
    :cvar U: UNKNOWN
    :cvar Z: Z_X_Y
    :cvar E: EXTENDS
    :cvar B: BBOX
    :cvar S: SCHEMATIC
    """

    U = "U"
    Z = "Z"
    E = "E"
    B = "B"
    S = "S"


class MatchAlgorithmType(Enum):
    AUTO = "AUTO"
    RTCM = "RTCM"
    INVERSE = "INVERSE"
    BOTH = "BOTH"


@dataclass
class MatchQualityType:
    avg_graph_distance: Optional[int] = field(
        default=None,
        metadata={
            "name": "avgGraphDistance",
            "type": "Attribute",
        },
    )
    max_graph_distance: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxGraphDistance",
            "type": "Attribute",
        },
    )
    avg_graph_time_distance: Optional[int] = field(
        default=None,
        metadata={
            "name": "avgGraphTimeDistance",
            "type": "Attribute",
        },
    )
    percent_coverage: Optional[int] = field(
        default=None,
        metadata={
            "name": "percentCoverage",
            "type": "Attribute",
        },
    )
    percent_track_coverage: Optional[int] = field(
        default=None,
        metadata={
            "name": "percentTrackCoverage",
            "type": "Attribute",
        },
    )
    percent_realtime: Optional[int] = field(
        default=None,
        metadata={
            "name": "percentRealtime",
            "type": "Attribute",
        },
    )
    check_in_quality: Optional[int] = field(
        default=None,
        metadata={
            "name": "checkInQuality",
            "type": "Attribute",
        },
    )
    check_out_quality: Optional[int] = field(
        default=None,
        metadata={
            "name": "checkOutQuality",
            "type": "Attribute",
        },
    )
    spatial_match: Optional[int] = field(
        default=None,
        metadata={
            "name": "spatialMatch",
            "type": "Attribute",
        },
    )
    time_spatial_match: Optional[int] = field(
        default=None,
        metadata={
            "name": "timeSpatialMatch",
            "type": "Attribute",
        },
    )
    overall_rating: Optional[int] = field(
        default=None,
        metadata={
            "name": "overallRating",
            "type": "Attribute",
        },
    )
    activity_match: Optional[int] = field(
        default=None,
        metadata={
            "name": "activityMatch",
            "type": "Attribute",
        },
    )
    vehicle_beacon_match: Optional[int] = field(
        default=None,
        metadata={
            "name": "vehicleBeaconMatch",
            "type": "Attribute",
        },
    )
    spatial_station_beacon_match: Optional[int] = field(
        default=None,
        metadata={
            "name": "spatialStationBeaconMatch",
            "type": "Attribute",
        },
    )


class MessageBaseType(Enum):
    """
    :cvar UNDEF: A more precise classification is not possible.
    :cvar GLOBAL: The HIM message is a global message.
    :cvar INFRASTRUCTURE: The HIM message is an infrastructural message.
    """

    UNDEF = "UNDEF"
    GLOBAL = "GLOBAL"
    INFRASTRUCTURE = "INFRASTRUCTURE"


@dataclass
class MessageCategoryType:
    """
    Message category having an ID and optional a name.

    :ivar id: ID of the HIM message category
    :ivar name: Localized name of the HIM message category
    """

    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MessageTextType:
    """
    :ivar tag: List of tags this message text is tagged with.
    :ivar text: List of text fragments.
    """

    tag: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )
    text: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )


@dataclass
class MobilityServiceProviderInfoType:
    """
    Region info.

    :ivar id: Id.
    :ivar ext_id: External id.
    :ivar name: Name.
    :ivar name_s: Short Name.
    :ivar abbreviation: Abbreviation.
    """

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "nameS",
            "type": "Attribute",
        },
    )
    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class NoteType(Enum):
    """
    :cvar U: Unknown
    :cvar A: Attribute
    :cvar I: Infotext
    :cvar R: Realtime
    :cvar H: Hint
    :cvar M: HIM-Message
    :cvar C: State of connection
    :cvar D: Reason for delay
    :cvar B: Through-connection
    :cvar Q: Freetext
    :cvar L: Reference train
    :cvar N: Connection specific realtime message
    :cvar O: Stop specific realtime message
    :cvar P: Train cancellation
    :cvar S: Change of train
    :cvar V: Change of product
    :cvar X: Extended platform change (e.g. change to different part of
        a station)
    :cvar Z: Change in itinerary (e.g. because of new or canceled stop)
    :cvar Y: Deviating origin or destination because of partial
        cancelation at start or end
    :cvar K: One entry of XI infotext
    :cvar G: Platform change
    :cvar W: Contains URL linking to a webview
    :cvar ED: DELFI/EU-SPIRIT: contains link to URL with additional
        information.
    :cvar TAR: Tariff specific hint
    :cvar FN: Product name based on raw data format
    :cvar TLN: Is typed location name
    :cvar LNC: Remark contains a component of the location name as
        defined in station raw data
    """

    U = "U"
    A = "A"
    I = "I"
    R = "R"
    H = "H"
    M = "M"
    C = "C"
    D = "D"
    B = "B"
    Q = "Q"
    L = "L"
    N = "N"
    O = "O"
    P = "P"
    S = "S"
    V = "V"
    X = "X"
    Z = "Z"
    Y = "Y"
    K = "K"
    G = "G"
    W = "W"
    ED = "ED"
    TAR = "TAR"
    FN = "FN"
    TLN = "TLN"
    LNC = "LNC"


@dataclass
class OccupancyType:
    """
    Occupany information.

    :ivar name: Name of seat class or category.
    :ivar v: Seat occupancy value of this class or category between 0
        and 100.
    :ivar number: Public number of the car for which the occupancy data
        is valid for, if the data is only valid for a single car.
        Otherwise this attribute is simply left out.
    :ivar raw: Seat occupancy raw data
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    v: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    raw: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class OperatorType:
    """
    Operator info.

    :ivar administration:
    :ivar name: Operator name for display.
    :ivar name_s: Operator name short.
    :ivar name_n: Operator name normal.
    :ivar name_l: Operator name long.
    :ivar add_name: Additional operator name.
    :ivar id: Identifier
    """

    administration: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "nameS",
            "type": "Attribute",
        },
    )
    name_n: Optional[str] = field(
        default=None,
        metadata={
            "name": "nameN",
            "type": "Attribute",
        },
    )
    name_l: Optional[str] = field(
        default=None,
        metadata={
            "name": "nameL",
            "type": "Attribute",
        },
    )
    add_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "addName",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class OriginDestTypeType(Enum):
    ST = "ST"
    ADR = "ADR"
    POI = "POI"
    CRD = "CRD"
    MCP = "MCP"
    HL = "HL"


class ParallelJourneyType(Enum):
    """
    :cvar UNDEF: Undefined type of parallel journey
    :cvar UNION: Parallel journey of type union
    :cvar THROUGHCOACH: Parallel journey of type throughcoach
    :cvar TIETHROUGH: Parallel journey of type tiethrough
    """

    UNDEF = "UNDEF"
    UNION = "UNION"
    THROUGHCOACH = "THROUGHCOACH"
    TIETHROUGH = "TIETHROUGH"


@dataclass
class PartialSearchReplacementType:
    """
    :ivar ctx: Set by the client depending on the selected partial
        search direction with the approriate context from a section of
        the trip response.
    :ivar suppl_chg_time: Supplementary change time at station to be
        considered as a minimum.
    """

    ctx: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 8096,
        },
    )
    suppl_chg_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "supplChgTime",
            "type": "Attribute",
        },
    )


class PlatformTypeType(Enum):
    """
    :cvar U: Undefinded
    :cvar PL: Platform/track at train station
    :cvar ST: Stop at bus or tram station
    :cvar GA: Terminal/Gate at airport
    :cvar PI: Pier if ship or ferry
    :cvar SL: Slot/parking space if bike or car
    :cvar FL: Floor in buildings or at footpath
    :cvar CI: Check-in/entrance
    :cvar CO: Check-out/exit
    :cvar X: No explicit type
    :cvar H: Hide platform information
    """

    U = "U"
    PL = "PL"
    ST = "ST"
    GA = "GA"
    PI = "PI"
    SL = "SL"
    FL = "FL"
    CI = "CI"
    CO = "CO"
    X = "X"
    H = "H"


@dataclass
class PolylineDesc:
    """
    Describes a polyline structure.

    :ivar crd: List of coordinates. Attribute "dim" defines how many
        items are used to build one coordinate tuple. In case of dim=3,
        z is in meter per default.
    :ivar name:
    :ivar delta: true: After the first item of the coordinates list only
        diff values are listed. false: list of coordinates contains
        complete coordinates.
    :ivar dim: Count of coordinate elements building one coordinate
        tuple. (2: x1, y1, x2, y2, ...; 3: x1, y1, z1, x2, y2, z2, ...)
    :ivar crd_enc_yx: Encoded YX coordinate values.
    :ivar crd_enc_z: Encoded Z coordinate values.
    :ivar crd_enc_s: Encoded quantifier.
    """

    crd: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    delta: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dim: int = field(
        default=2,
        metadata={
            "type": "Attribute",
        },
    )
    crd_enc_yx: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncYX",
            "type": "Attribute",
        },
    )
    crd_enc_z: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncZ",
            "type": "Attribute",
        },
    )
    crd_enc_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncS",
            "type": "Attribute",
        },
    )


class PolylineEncodingType(Enum):
    N = "N"
    DLT = "DLT"
    GPA = "GPA"


class PreselectionEdgeTypeErr(Enum):
    """
    :cvar OK: Success. No error occured.
    :cvar NO_RESULT: Using the specified constraints no route could be
        found.
    """

    OK = "OK"
    NO_RESULT = "NO_RESULT"


class PrognosisType(Enum):
    """
    PrognosisType provides the type of the prognosis like if the prognosis was
    reported by an external provider or calculated or corrected by the system.

    :cvar PROGNOSED: Prognosis was reported from an external provider as
        a prognosis for the future.
    :cvar MANUAL: Prognosis was reported from an external provider from
        a manual entry.
    :cvar REPORTED: Prognosis was reported from an external provider as
        a delay for previously passed stations.
    :cvar CORRECTED: Prognosis was corrected by the system to adjust the
        prognoses over the train's journey to ensure proper
        continuation.
    :cvar CALCULATED: Prognosis was calculated by the system for
        upcoming stations or to fill gaps for previously passed stations
        where no delay was reported.
    """

    PROGNOSED = "PROGNOSED"
    MANUAL = "MANUAL"
    REPORTED = "REPORTED"
    CORRECTED = "CORRECTED"
    CALCULATED = "CALCULATED"


@dataclass
class RgbacolorType:
    """
    :ivar r: Red
    :ivar g: Green
    :ivar b: Blue
    :ivar a: Alpha
    :ivar hex:
    """

    class Meta:
        name = "RGBAColorType"

    r: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 255,
        },
    )
    g: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 255,
        },
    )
    b: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 255,
        },
    )
    a: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 255,
        },
    )
    hex: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"#[\dA-F]{6}([\dA-F][\dA-F])?",
        },
    )


class RealtimeDataSourceType(Enum):
    """
    :cvar DEFAULT: Default source (undefined)
    :cvar VDV:
    :cvar HIM:
    :cvar HRC:
    :cvar SIRI:
    :cvar UIC:
    :cvar HRX:
    :cvar GTFS:
    :cvar FIS:
    :cvar DDS: Datendrehscheiben
    :cvar PAISA: PA-ISA
    :cvar FE: FahrtenEditor
    :cvar BLACKLIST: List of blacklisted trains
    :cvar ARAMIS: ARAMIS data source
    :cvar RTABO2: RTABO2 data source
    """

    DEFAULT = "DEFAULT"
    VDV = "VDV"
    HIM = "HIM"
    HRC = "HRC"
    SIRI = "SIRI"
    UIC = "UIC"
    HRX = "HRX"
    GTFS = "GTFS"
    FIS = "FIS"
    DDS = "DDS"
    PAISA = "PAISA"
    FE = "FE"
    BLACKLIST = "BLACKLIST"
    ARAMIS = "ARAMIS"
    RTABO2 = "RTABO2"


class ReconstructionConversionModeType(Enum):
    """
    :cvar TO_CGI_LEGACY: Convert to version 1.
    """

    TO_CGI_LEGACY = "TO_CGI_LEGACY"


class ReconstructionSectionType(Enum):
    """
    :cvar JNY:
    :cvar WALK:
    :cvar TRSF: Transfer
    :cvar DEVI: Deviation
    :cvar GIS_FOOT: On foot (based on GIS)
    :cvar GIS_BIKE: Bike (based on GIS)
    :cvar GIS_PARK: Park &amp; Ride (based on GIS)
    :cvar GIS_KISS: Kiss &amp; Ride (based on GIS)
    :cvar GIS_TAXI: Taxi (based on GIS)
    """

    JNY = "JNY"
    WALK = "WALK"
    TRSF = "TRSF"
    DEVI = "DEVI"
    GIS_FOOT = "GIS_FOOT"
    GIS_BIKE = "GIS_BIKE"
    GIS_PARK = "GIS_PARK"
    GIS_KISS = "GIS_KISS"
    GIS_TAXI = "GIS_TAXI"


class ReconstructionStateType(Enum):
    """
    Contains the outcome information for the section, if it resulted from a
    reconstruction.

    :cvar U: Reconstruction state not set. Original connection or
        section.
    :cvar C: Connection or section was successfully reconstructed
        completely.
    :cvar P: Connection was partially reconstructed and might contain
        dummy sections filled with data from the input reconstruction
        context, if enabled in the request.
    :cvar N: Connection or section was not reconstructable. In case of
        section, the section might be filled with data from the input
        reconstruction context, if enabled in the request.
    :cvar O: Original connection or section from a trip search.
    """

    U = "U"
    C = "C"
    P = "P"
    N = "N"
    O = "O"


class ReferencedJourneyTypeType(Enum):
    UNDEF = "UNDEF"
    DEFAULT = "DEFAULT"
    IST_ERSATZFAHRT = "IST_ERSATZFAHRT"
    IST_VERSTAERKERFAHRT = "IST_VERSTAERKERFAHRT"
    IST_FORTFUEHRUNG = "IST_FORTFUEHRUNG"
    IST_TRENNUNG = "IST_TRENNUNG"
    IST_FORTFUEHRUNG_VON_TRENNUNG = "IST_FORTFUEHRUNG_VON_TRENNUNG"
    IST_ZUSAMMENFUEHRUNG = "IST_ZUSAMMENFUEHRUNG"
    IST_FORTFUEHRUNG_DURCH_ZUSAMMENFUEHRUNG = (
        "IST_FORTFUEHRUNG_DURCH_ZUSAMMENFUEHRUNG"
    )
    IST_ENTLASTUNG = "IST_ENTLASTUNG"
    DEFAULT_R = "DEFAULT_R"
    HAT_ERSATZFAHRT = "HAT_ERSATZFAHRT"
    HAT_VERSTAERKERFAHRT = "HAT_VERSTAERKERFAHRT"
    HAT_FORTFUEHRUNG = "HAT_FORTFUEHRUNG"
    HAT_TRENNUNG = "HAT_TRENNUNG"
    HAT_FORTFUEHRUNG_VON_TRENNUNG = "HAT_FORTFUEHRUNG_VON_TRENNUNG"
    HAT_ZUSAMMENFUEHRUNG = "HAT_ZUSAMMENFUEHRUNG"
    HAT_FORTFUEHRUNG_DURCH_ZUSAMMENFUEHRUNG = (
        "HAT_FORTFUEHRUNG_DURCH_ZUSAMMENFUEHRUNG"
    )
    HAT_ENTLASTUNG = "HAT_ENTLASTUNG"


@dataclass
class RegionType:
    """
    Region info.

    :ivar name: Name.
    :ivar ext_id: External ID.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ext_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ResourceLinkType:
    rel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
class ResultStatusType:
    """
    :ivar time_diff_critical: Based on the configuration, a critical
        time difference between connections in the result has been
        detected.
    """

    time_diff_critical: bool = field(
        default=False,
        metadata={
            "name": "timeDiffCritical",
            "type": "Attribute",
        },
    )


@dataclass
class Ring:
    """Ring structure.

    If minRadius is unset or zero, it is describes a circle.

    :ivar lon: Longitude
    :ivar lat: Latitude
    :ivar min_radius: Minimum radius in meter.
    :ivar max_radius: Maximum radius in meter.
    """

    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    min_radius: Optional[int] = field(
        default=None,
        metadata={
            "name": "minRadius",
            "type": "Attribute",
        },
    )
    max_radius: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxRadius",
            "type": "Attribute",
        },
    )


class RtModeType(Enum):
    """
    :cvar SERVER_DEFAULT: One of the following modes is configured in
        the HAFAS server back end.
    :cvar OFF: Search on planned data, ignore real-time information
        completely: Connections are computed on the basis of planned
        data. No real-time information is shown.
    :cvar INFOS: Search on planned data, use real-time information for
        display only: Connections are computed on the basis of planned
        data. Delays and feasibility of the connections are integrated
        into the result. Note that additional trains (supplied via
        realtime feed) will not be part of the resulting connections.
    :cvar FULL: Combined search on planned and real-time data. This
        search consists of two steps: i. Search on scheduled data, ii.
        If the result of step (i) contains a non-feasible connection, a
        search on real-time data is performed and all results are
        combined.
    :cvar REALTIME: Search on real-time data: Connections are computed
        on the basis of real-time data, using planned schedule only
        whenever no real-time data is available. All connections
        computed are feasible with respect to the currently known real-
        time situation. Additional trains (supplied via real-time feed)
        will be found if these are part of a fast, comfortable, or
        direct connection (or economic connection, if economic search is
        activated).
    """

    SERVER_DEFAULT = "SERVER_DEFAULT"
    OFF = "OFF"
    INFOS = "INFOS"
    FULL = "FULL"
    REALTIME = "REALTIME"


@dataclass
class ServiceDays:
    """Regular service days describe a regular set of days.

    Irregular service days describe a different schedule of days.

    :ivar planning_period_begin: Start of the planning period of this
        data in format YYYY-MM-DD.
    :ivar planning_period_end: End of the planning period of this data
        in format YYYY-MM-DD.
    :ivar s_days_r: Regular service days.
    :ivar s_days_i: Irregular service days.
    :ivar s_days_b: Bit field of the service days in hex representation
    :ivar route_idx_from: First stop/station where this note is valid.
        See the Stops list in the JourneyDetail response for this leg to
        get more details about this stop/station.
    :ivar route_idx_to: Last stop/station where this note is valid. See
        the Stops list in the JourneyDetail response for this leg to get
        more details about this stop/station.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    planning_period_begin: Optional[str] = field(
        default=None,
        metadata={
            "name": "planningPeriodBegin",
            "type": "Attribute",
        },
    )
    planning_period_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "planningPeriodEnd",
            "type": "Attribute",
        },
    )
    s_days_r: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDaysR",
            "type": "Attribute",
        },
    )
    s_days_i: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDaysI",
            "type": "Attribute",
        },
    )
    s_days_b: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDaysB",
            "type": "Attribute",
        },
    )
    route_idx_from: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )


class SotContextLocModeType(Enum):
    """
    :cvar UNKNOWN: Position: Location unknown.
    :cvar FROM_START: Position: At start of trip before departure.
    :cvar IN_TRAIN: Position: In service.
    :cvar AT_PASSED_STOP: Position: At passed stop.
    :cvar AT_CHANGE_STOP: Position: At interchange location.
    :cvar BEFORE_TRAVEL: Position: Before start of trip, not at
        departure stop.
    :cvar AT_DESTINATION: Position: At destination.
    :cvar ERROR: Common error during calculation of position.
    :cvar ERROR_SEARCH_FROM_TRAIN_BEFORE_START: Search on trip before
        departure of service.
    :cvar ERROR_IN_RECONSTRUCTION: Error during reconstruction. No
        postion calculation possible.
    :cvar TO_BE_DEFINED_IN_SERVER: Certain state during calculation.
    :cvar ERROR_TRAIN_CANCELLED: Serice cancelled.
    :cvar CHECK_COMPLETE_TRAIN: Certain state during calculation.
    :cvar AT_LAST_USABLE_STOP: Position: At last possible start.
    :cvar ERROR_ALL_TRAINS_FILTERED: All alternative connections
        filtered.
    :cvar ERROR_STAY_IN_CURRENT_CONNECTION: Stay in service. No better
        alternatives found.
    """

    UNKNOWN = "UNKNOWN"
    FROM_START = "FROM_START"
    IN_TRAIN = "IN_TRAIN"
    AT_PASSED_STOP = "AT_PASSED_STOP"
    AT_CHANGE_STOP = "AT_CHANGE_STOP"
    BEFORE_TRAVEL = "BEFORE_TRAVEL"
    AT_DESTINATION = "AT_DESTINATION"
    ERROR = "ERROR"
    ERROR_SEARCH_FROM_TRAIN_BEFORE_START = (
        "ERROR_SEARCH_FROM_TRAIN_BEFORE_START"
    )
    ERROR_IN_RECONSTRUCTION = "ERROR_IN_RECONSTRUCTION"
    TO_BE_DEFINED_IN_SERVER = "TO_BE_DEFINED_IN_SERVER"
    ERROR_TRAIN_CANCELLED = "ERROR_TRAIN_CANCELLED"
    CHECK_COMPLETE_TRAIN = "CHECK_COMPLETE_TRAIN"
    AT_LAST_USABLE_STOP = "AT_LAST_USABLE_STOP"
    ERROR_ALL_TRAINS_FILTERED = "ERROR_ALL_TRAINS_FILTERED"
    ERROR_STAY_IN_CURRENT_CONNECTION = "ERROR_STAY_IN_CURRENT_CONNECTION"


@dataclass
class TagsType:
    """
    :ivar tag: List of tags.
    """

    tag: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )


@dataclass
class TechnicalMessage:
    """Can contain any technical message by either the API server itself or any
    backend system involved.

    The content is not part of the functional response and can be seen
    as metadata.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class TimetableInfoTypeType(Enum):
    U = "U"
    ST = "ST"
    ADR = "ADR"
    POI = "POI"


class TrackPoinSourceType(Enum):
    BEACON = "BEACON"
    GPS = "GPS"
    MOBILE = "MOBILE"


class TrafficMessageTypeType(Enum):
    """
    Type of traffic message.

    :cvar U: Unknown
    :cvar RCLM: maintenance work
    :cvar AC: accident
    :cvar RW: construction work
    :cvar AT: high traffic volume
    :cvar CO: other circumstances
    :cvar TRAFFIC_JAM: traffic jam
    :cvar DELAY: delay
    :cvar ROAD_CLOSED: road closed
    :cvar JUNCTION_CLOSED: junction closed
    :cvar LANE_CLOSED: lane closed
    :cvar BURNING_VEHICLE: burning vehicle
    :cvar ACCIDENT: accident
    :cvar DANGER: danger
    :cvar OBSTRUCTION: obstruction
    :cvar RAIL_ROAD_CROSSING: railroad crossing
    :cvar TRAFFIC_LIGHTS_DEFECT: traffic lights defect
    :cvar WEATHER: generic weather event
    :cvar WEATHER_ICE: ice
    :cvar WEATHER_SNOW: snow
    :cvar WEATHER_POOR_VISIBILITY: poor visibility
    :cvar WEATHER_HAIL: hail
    :cvar WEATHER_WIND: wind
    :cvar CONSTRUCTION_SITE: construction site
    """

    U = "U"
    RCLM = "RCLM"
    AC = "AC"
    RW = "RW"
    AT = "AT"
    CO = "CO"
    TRAFFIC_JAM = "TRAFFIC_JAM"
    DELAY = "DELAY"
    ROAD_CLOSED = "ROAD_CLOSED"
    JUNCTION_CLOSED = "JUNCTION_CLOSED"
    LANE_CLOSED = "LANE_CLOSED"
    BURNING_VEHICLE = "BURNING_VEHICLE"
    ACCIDENT = "ACCIDENT"
    DANGER = "DANGER"
    OBSTRUCTION = "OBSTRUCTION"
    RAIL_ROAD_CROSSING = "RAIL_ROAD_CROSSING"
    TRAFFIC_LIGHTS_DEFECT = "TRAFFIC_LIGHTS_DEFECT"
    WEATHER = "WEATHER"
    WEATHER_ICE = "WEATHER_ICE"
    WEATHER_SNOW = "WEATHER_SNOW"
    WEATHER_POOR_VISIBILITY = "WEATHER_POOR_VISIBILITY"
    WEATHER_HAIL = "WEATHER_HAIL"
    WEATHER_WIND = "WEATHER_WIND"
    CONSTRUCTION_SITE = "CONSTRUCTION_SITE"


@dataclass
class TravellerProfileType:
    data: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "max_length": 32768,
        },
    )


class TripSearchFilterTypeBikeCarriageType(Enum):
    SINGLEBIKES = "SINGLEBIKES"
    SMALLGROUPS = "SMALLGROUPS"
    LARGEGROUPS = "LARGEGROUPS"


@dataclass
class TripStatusType:
    """
    :ivar detour: Connection having detour
    :ivar daily: Daily
    :ivar direct: Direct connection
    :ivar sub_optimal_direct: Suboptimal direct connection
    :ivar slow_direct: Overtaken/slower direct connection
    :ivar economic: Economic connection
    :ivar convenient: Convenient connection
    :ivar specialtrain: Special train
    :ivar uk_national_routeing_guide_failure: Connection is not conform
        to "UK National Routeing Guide".
    :ivar hint: Hint
    :ivar hint_code: 510 ( Unvollstaendige Rekonstruktion ) 500 (
        zuviele Zuege, Ausgabe gekuerzt ) 480 ( Geocodierungswarnung,
        allgemein ) 481 ( Geocodierungswarnung am Start ) 482 (
        Geocodierungswarnung am Ziel ) 460 ( Bahnhof mehrfach bedient in
        Verb. ) 455 ( Langer Aufenthalt auf einem Bf ) 456 ( Verb.
        erreicht ein Land mehrmals ) 410 ( Zugangebot durch
        Fahrplanwechsel nicht vollstaendig ) 390 ( aequivalente
        Haltestelle gewaehlt )
    :ivar unsharp: Connection resulted from an unsharp search
    :ivar time_diff_critical: Based on the configuration, this
        connection has a critical time difference, either to the search
        date/time or to a previous/subsequent connection.
    """

    detour: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    daily: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    direct: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    sub_optimal_direct: bool = field(
        default=False,
        metadata={
            "name": "subOptimalDirect",
            "type": "Attribute",
        },
    )
    slow_direct: bool = field(
        default=False,
        metadata={
            "name": "slowDirect",
            "type": "Attribute",
        },
    )
    economic: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    convenient: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    specialtrain: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    uk_national_routeing_guide_failure: bool = field(
        default=False,
        metadata={
            "name": "ukNationalRouteingGuideFailure",
            "type": "Attribute",
        },
    )
    hint: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hint_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "hintCode",
            "type": "Attribute",
        },
    )
    unsharp: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    time_diff_critical: bool = field(
        default=False,
        metadata={
            "name": "timeDiffCritical",
            "type": "Attribute",
        },
    )


@dataclass
class UrlLinkType:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ViaStatusType(Enum):
    EXR = "EXR"
    NER = "NER"
    NEXR = "NEXR"
    NXR = "NXR"


@dataclass
class Warning:
    """
    Warning.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class WeatherType(Enum):
    """
    Type of weather.

    :cvar UNDEF: undefined
    :cvar CLEAR: clear
    :cvar PARTIALLY_CLOUDY: partially cloudy
    :cvar CLOUDY: cloudy
    :cvar RAIN: rain
    :cvar HEAVY_RAIN: heavy rain
    :cvar SNOW: snow
    :cvar HEAVY_SNOW: heavy snow
    :cvar HAIL: hail
    :cvar HEAVY_HAIL: heavy hail
    :cvar FOG: fog
    :cvar THUNDERSTORM: thunderstorm
    :cvar STORM: storm
    :cvar SLIGHTLY_CLOUDY: slightly cloudy
    :cvar SLEET: sleet
    :cvar RAIN_SHOWER: rain shower
    :cvar SNOW_SHOWER: snow shower
    :cvar SLEET_SHOWER: sleet shower
    :cvar HEAVY_FOG: heavy fog
    :cvar SLIPPERY_ROAD: slippery road
    :cvar DRIZZLE: drizzle
    :cvar WET_AND_COLD: wet and cold
    :cvar DRY: dry
    :cvar SANDSTORM: sandstorm
    :cvar HEAVY_SANDSTORM: heavy sandstorm
    :cvar THUNDER_SANDSTORM: thunder sandstorm
    """

    UNDEF = "UNDEF"
    CLEAR = "CLEAR"
    PARTIALLY_CLOUDY = "PARTIALLY_CLOUDY"
    CLOUDY = "CLOUDY"
    RAIN = "RAIN"
    HEAVY_RAIN = "HEAVY_RAIN"
    SNOW = "SNOW"
    HEAVY_SNOW = "HEAVY_SNOW"
    HAIL = "HAIL"
    HEAVY_HAIL = "HEAVY_HAIL"
    FOG = "FOG"
    THUNDERSTORM = "THUNDERSTORM"
    STORM = "STORM"
    SLIGHTLY_CLOUDY = "SLIGHTLY_CLOUDY"
    SLEET = "SLEET"
    RAIN_SHOWER = "RAIN_SHOWER"
    SNOW_SHOWER = "SNOW_SHOWER"
    SLEET_SHOWER = "SLEET_SHOWER"
    HEAVY_FOG = "HEAVY_FOG"
    SLIPPERY_ROAD = "SLIPPERY_ROAD"
    DRIZZLE = "DRIZZLE"
    WET_AND_COLD = "WET_AND_COLD"
    DRY = "DRY"
    SANDSTORM = "SANDSTORM"
    HEAVY_SANDSTORM = "HEAVY_SANDSTORM"
    THUNDER_SANDSTORM = "THUNDER_SANDSTORM"


@dataclass
class PricingType:
    class Meta:
        name = "pricingType"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
    idx: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ConnectionReliabilityType:
    """
    :ivar original: Reliability of the connection itself regarding its
        realtime status including cancellations, delays etc. to the get
        to the destination in time. Used in time machine feature.
    :ivar alternative: Reliability of an alternative connection to the
        original connection regarding its realtime status including
        cancellations, delays etc. Used in time machine feature.
    """

    original: Optional[ConnectionReliabilityValueType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alternative: Optional[ConnectionReliabilityValueType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Directions:
    """
    The list of journey directions.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    direction: List[Direction] = field(
        default_factory=list,
        metadata={
            "name": "Direction",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class GeoDataType:
    """
    :ivar id: External ID of the data.
    :ivar type_value: Type of geo data.
    :ivar data: Geo data of the given type.
    :ivar min_zoom: Minimal zoom level for displaying the geometries.
    :ivar max_zoom: Maximum zoom level up until which geometries should
        be displayed.
    """

    id: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[GeoDataTypeType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    data: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    min_zoom: Optional[int] = field(
        default=None,
        metadata={
            "name": "minZoom",
            "type": "Attribute",
        },
    )
    max_zoom: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxZoom",
            "type": "Attribute",
        },
    )


@dataclass
class GisProfile:
    """
    :ivar router_option: Passed through GIS router specific option.
    :ivar attribute: Filter locations by attribute code. If the
        attribute should not be part of the be location data, negate it
        by putting ! in front of it.
    :ivar type_value: Type of referenced GIS profile (foot, bike...)
    :ivar applies_to:
    :ivar min_dist: Minimum distance in meters.
    :ivar max_dist: Maximum distance in meter.
    :ivar speed: Speed value to be used. &lt; 100: faster; = 100: normal
        (default); &gt; 100: slower
    :ivar beeline: Bee line routing instead of using external GIS
        router.
    """

    router_option: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "routerOption",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    attribute: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "max_length": 128,
        },
    )
    type_value: Optional[GisProfileType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    applies_to: Optional[ApplyToType] = field(
        default=None,
        metadata={
            "name": "appliesTo",
            "type": "Attribute",
            "required": True,
        },
    )
    min_dist: Optional[int] = field(
        default=None,
        metadata={
            "name": "minDist",
            "type": "Attribute",
        },
    )
    max_dist: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxDist",
            "type": "Attribute",
        },
    )
    speed: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    beeline: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class IconType:
    """
    :ivar foreground_color: Text color
    :ivar background_color: Background color
    :ivar border_color: Border color
    :ivar res: Resource description or name
    :ivar txt: Text
    :ivar txt_s: Short text
    :ivar style: Text style
    :ivar shape: Icon shape
    :ivar shape_res: Shape description. Only relevant if @shape equals
        RES
    """

    foreground_color: Optional[RgbacolorType] = field(
        default=None,
        metadata={
            "name": "foregroundColor",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    background_color: Optional[RgbacolorType] = field(
        default=None,
        metadata={
            "name": "backgroundColor",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    border_color: Optional[RgbacolorType] = field(
        default=None,
        metadata={
            "name": "borderColor",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    res: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    txt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    txt_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtS",
            "type": "Attribute",
        },
    )
    style: IconStyleType = field(
        default=IconStyleType.U,
        metadata={
            "type": "Attribute",
        },
    )
    shape: IconShapeType = field(
        default=IconShapeType.U,
        metadata={
            "type": "Attribute",
        },
    )
    shape_res: Optional[str] = field(
        default=None,
        metadata={
            "name": "shapeRes",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyPathItemType:
    """
    :ivar progress_in_time: Milliseconds after request.
    :ivar progress_in_percent: Progress between from and to location in
        percent.
    :ivar progress_abs: Progress between from and to location in meter.
    :ivar from_location_id: Location reference by ID.
    :ivar to_location_id: Location reference by ID.
    :ivar dir_geo: Geographical direction of the route. The direction
        range is from 0 to 31 with 0 starting from the x-axis in
        mathematical positive direction.
    :ivar state: State, if journey is before, on or after relevant
        segment.
    """

    progress_in_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "progressInTime",
            "type": "Attribute",
        },
    )
    progress_in_percent: Optional[int] = field(
        default=None,
        metadata={
            "name": "progressInPercent",
            "type": "Attribute",
        },
    )
    progress_abs: Optional[int] = field(
        default=None,
        metadata={
            "name": "progressAbs",
            "type": "Attribute",
        },
    )
    from_location_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fromLocationId",
            "type": "Attribute",
        },
    )
    to_location_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "toLocationId",
            "type": "Attribute",
        },
    )
    dir_geo: Optional[int] = field(
        default=None,
        metadata={
            "name": "dirGeo",
            "type": "Attribute",
        },
    )
    state: JourneyPathItemStateType = field(
        default=JourneyPathItemStateType.U,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class JourneyStatus:
    """
    Contains the status of the journey.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    value: Optional[JourneyStatusValue] = field(default=None)


@dataclass
class JourneyValidation:
    """
    Result of a JorneyValidation request.

    :ivar item: A list of validated trains. Name is the train number.
        Value is true, if JourneyPos information are available
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    item: List[BooleanKvtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class LocationNote:
    """
    Text to be displayed.

    :ivar value:
    :ivar key: An identifier of this note.
    :ivar type_value: The type of this note.
    :ivar txt_n: Normal version of this notes text
    :ivar txt_l: Long version of this notes text
    :ivar txt_s: Short version of this notes text
    :ivar url: URL for this note
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: NoteType = field(
        default=NoteType.U,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    txt_n: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtN",
            "type": "Attribute",
        },
    )
    txt_l: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtL",
            "type": "Attribute",
        },
    )
    txt_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtS",
            "type": "Attribute",
        },
    )
    url: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MessageChannelType:
    """
    :ivar name: Name of the channel.
    :ivar url: URL to external content of this message channel.
    :ivar valid_from_time: In this channel, the message is valid
        beginning at time in format hh:mm[:ss]
    :ivar valid_from_date: In this channel, the message is valid
        beginning at date in format YYYY-MM-DD.
    :ivar valid_to_time: In this channel, the message is valid ending at
        time in format hh:mm[:ss]
    :ivar valid_to_date: In this channel, the message is valid ending at
        date in format YYYY-MM-DD.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    url: List[UrlLinkType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    valid_from_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "validFromTime",
            "type": "Attribute",
        },
    )
    valid_from_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "validFromDate",
            "type": "Attribute",
        },
    )
    valid_to_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "validToTime",
            "type": "Attribute",
        },
    )
    valid_to_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "validToDate",
            "type": "Attribute",
        },
    )


@dataclass
class Note:
    """
    Note to be displayed.

    :ivar value:
    :ivar key: An identifier of this note.
    :ivar type_value: The type of this note.
    :ivar priority: The priority of this note. A lower priority value
        means a higher importance.
    :ivar url: URL for this note
    :ivar route_idx_from: First stop/station where this note is valid.
        See the Stops list in the JourneyDetail response for this leg to
        get more details about this stop/station.
    :ivar route_idx_to: Last stop/station where this note is valid. See
        the Stops list in the JourneyDetail response for this leg to get
        more details about this stop/station.
    :ivar txt_n: Normal version of this notes text
    :ivar txt_l: Long version of this notes text
    :ivar txt_s: Short version of this notes text
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    key: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: NoteType = field(
        default=NoteType.U,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    priority: int = field(
        default=100,
        metadata={
            "type": "Attribute",
        },
    )
    url: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx_from: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )
    txt_n: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtN",
            "type": "Attribute",
        },
    )
    txt_l: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtL",
            "type": "Attribute",
        },
    )
    txt_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "txtS",
            "type": "Attribute",
        },
    )


@dataclass
class OutputControlType:
    """
    :ivar poly:
    :ivar poly_enc:
    :ivar passlist:
    :ivar show_passing_points:
    :ivar iv_only:
    :ivar iv_include:
    :ivar eco:
    :ivar eco_cmp:
    :ivar eco_params:
    :ivar baim:
    :ivar with_journey_boundary_points: Enables/disables the return of
        journey boundary stops at public transport legs.
    """

    poly: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    poly_enc: Optional[PolylineEncodingType] = field(
        default=None,
        metadata={
            "name": "polyEnc",
            "type": "Attribute",
        },
    )
    passlist: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    show_passing_points: bool = field(
        default=False,
        metadata={
            "name": "showPassingPoints",
            "type": "Attribute",
        },
    )
    iv_only: bool = field(
        default=False,
        metadata={
            "name": "ivOnly",
            "type": "Attribute",
        },
    )
    iv_include: bool = field(
        default=False,
        metadata={
            "name": "ivInclude",
            "type": "Attribute",
        },
    )
    eco: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    eco_cmp: bool = field(
        default=False,
        metadata={
            "name": "ecoCmp",
            "type": "Attribute",
        },
    )
    eco_params: Optional[str] = field(
        default=None,
        metadata={
            "name": "ecoParams",
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    baim: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    with_journey_boundary_points: bool = field(
        default=False,
        metadata={
            "name": "withJourneyBoundaryPoints",
            "type": "Attribute",
        },
    )


@dataclass
class PlatformType:
    """
    Platform information.

    :ivar alt_id:
    :ivar type_value: Display text.
    :ivar text: Display text.
    :ivar hidden: True if track information is marked as hidden.
    :ivar lon: The WGS84 longitude of the geographical position.
    :ivar lat: The WGS84 latitude of the geographical position.
    :ivar alt: The altitude of the geographical position.
    """

    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    type_value: PlatformTypeType = field(
        default=PlatformTypeType.U,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Polyline:
    """
    :ivar crd: List of coordinates. Attribute "dim" defines how many
        items are used to build one coordinate tuple.
    :ivar name:
    :ivar delta: true: After the first item of the coordinates list only
        diff values are listed. false: list of coordinates contains
        complete coordinates.
    :ivar dim: Count of coordinate elements building one coordinate
        tuple. (2: x1, y1, x2, y2, ...; 3: x1, y1, z1, x2, y2, z2, ...)
    :ivar type_value:
    :ivar crd_enc_yx: Encoded YX coordinate values.
    :ivar crd_enc_z: Encoded Z coordinate values.
    :ivar crd_enc_s: Encoded quantifier.
    """

    crd: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    delta: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dim: int = field(
        default=2,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: CoordType = field(
        default=CoordType.WGS84,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    crd_enc_yx: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncYX",
            "type": "Attribute",
        },
    )
    crd_enc_z: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncZ",
            "type": "Attribute",
        },
    )
    crd_enc_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "crdEncS",
            "type": "Attribute",
        },
    )


@dataclass
class PolylineGroup:
    """
    :ivar polyline_desc: List of polyline descriptions.
    :ivar name:
    :ivar coord_type: Type of coordinate system.
    :ivar layer_name: Display name of layer.
    """

    polyline_desc: List[PolylineDesc] = field(
        default_factory=list,
        metadata={
            "name": "polylineDesc",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    coord_type: CoordType = field(
        default=CoordType.WGS84,
        metadata={
            "name": "coordType",
            "type": "Attribute",
        },
    )
    layer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "layerName",
            "type": "Attribute",
        },
    )


@dataclass
class PreselectionEdgeType:
    """
    :ivar id: Unique ID that will be attached to all sections that
        resulted from this edge.
    :ivar duration: Overall duration for this edge between reference
        point and preselected node in minutes.
    :ivar dist: Overall distance for this edge in meters between
        reference point and preselected node.
    :ivar value: Number of virtual changes assumed for this edge. Used
        for change optimized trips.
    :ivar speed: Speed value to be used. &lt; 100: faster; = 100: normal
        (default); &gt; 100: slower
    :ivar cost: Ranking value within the location list to be used
    :ivar err: Ranking value within the location list to be used
    """

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    duration: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    speed: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cost: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    err: PreselectionEdgeTypeErr = field(
        default=PreselectionEdgeTypeErr.OK,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ReconstructionConvertRequest:
    """
    Requests the conversion of reconstruction contexts.

    :ivar ctx: Reconstruction context to be converted.
    :ivar mode: What the reconstruction converter should do.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ctx: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_length": 32768,
        },
    )
    mode: ReconstructionConversionModeType = field(
        default=ReconstructionConversionModeType.TO_CGI_LEGACY,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Rect:
    """
    Rectangle structure.

    :ivar ll_crd: Lower left coordinate.
    :ivar ur_crd: Upper right coordinate.
    """

    ll_crd: Optional[Coordinate] = field(
        default=None,
        metadata={
            "name": "llCrd",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    ur_crd: Optional[Coordinate] = field(
        default=None,
        metadata={
            "name": "urCrd",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )


@dataclass
class ResourceLinks:
    link: List[ResourceLinkType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class SearchOptionsType:
    """
    :ivar blocking:
    :ivar num_b:
    :ivar num_f:
    :ivar context: Defines the starting point for the scroll back or
        forth operation. Use the scrB value from a previous result to
        scroll backwards in time and use the scrF value to scroll forth.
    :ivar change_time_percent:
    :ivar min_change_time:
    :ivar max_change_time:
    :ivar add_change_time:
    :ivar max_changes:
    :ivar search_for_arrival:
    :ivar rt_mode:
    :ivar unsharp:
    :ivar economic:
    :ivar include_earlier:
    :ivar with_ictalternatives:
    """

    blocking: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    num_b: int = field(
        default=0,
        metadata={
            "name": "numB",
            "type": "Attribute",
        },
    )
    num_f: int = field(
        default=5,
        metadata={
            "name": "numF",
            "type": "Attribute",
        },
    )
    context: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 8096,
        },
    )
    change_time_percent: Optional[int] = field(
        default=None,
        metadata={
            "name": "changeTimePercent",
            "type": "Attribute",
        },
    )
    min_change_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "minChangeTime",
            "type": "Attribute",
        },
    )
    max_change_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxChangeTime",
            "type": "Attribute",
        },
    )
    add_change_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "addChangeTime",
            "type": "Attribute",
        },
    )
    max_changes: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxChanges",
            "type": "Attribute",
        },
    )
    search_for_arrival: bool = field(
        default=False,
        metadata={
            "name": "searchForArrival",
            "type": "Attribute",
        },
    )
    rt_mode: RtModeType = field(
        default=RtModeType.SERVER_DEFAULT,
        metadata={
            "name": "rtMode",
            "type": "Attribute",
        },
    )
    unsharp: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    economic: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    include_earlier: bool = field(
        default=False,
        metadata={
            "name": "includeEarlier",
            "type": "Attribute",
        },
    )
    with_ictalternatives: bool = field(
        default=False,
        metadata={
            "name": "withICTAlternatives",
            "type": "Attribute",
        },
    )


@dataclass
class SotContextType:
    """
    :ivar calc_date: Date of calculation.
    :ivar calc_time: time of calculation.
    :ivar journey_id: Contains an internal journey id used for a
        subsequent journey detail request.
    :ivar train_name: Name of service.
    :ivar leg_idx: Index of leg for the calculated position in the trip.
    :ivar leg_idx_foot_path_connection: Index of leg connected by foot
        path.
    :ivar prev_loc_route_idx: Index of last passed stop.
    :ivar cur_loc_route_idx: Index of current or next stop.
    :ivar loc_route_idx_foot_path_connection: Index of stop connected by
        foot path.
    :ivar loc_mode:
    """

    calc_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "calcDate",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    calc_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "calcTime",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "journeyId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    train_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainName",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    leg_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "legIdx",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    leg_idx_foot_path_connection: Optional[int] = field(
        default=None,
        metadata={
            "name": "legIdxFootPathConnection",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    prev_loc_route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "prevLocRouteIdx",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    cur_loc_route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "curLocRouteIdx",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    loc_route_idx_foot_path_connection: Optional[int] = field(
        default=None,
        metadata={
            "name": "locRouteIdxFootPathConnection",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    loc_mode: Optional[SotContextLocModeType] = field(
        default=None,
        metadata={
            "name": "locMode",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )


@dataclass
class TechnicalMessages:
    """
    Can contain any number of technical messages.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    technical_message: List[TechnicalMessage] = field(
        default_factory=list,
        metadata={
            "name": "TechnicalMessage",
            "type": "Element",
        },
    )


@dataclass
class TimetableInfoType:
    """
    :ivar pool_id: Pool id.
    :ivar date: Date of pool creation.
    :ivar time: Time of pool creation.
    :ivar ident: Checksum for pool.
    :ivar comment: Comment of the pool data.
    :ivar type_value: The attribute type specifies the type of the time
        table. Valid values are ST (stop/station), ADR (address) or POI
        (point of interest). If not specified, U (unknown) is returned.
    :ivar begin: Start date of the pool data timetable period.
    :ivar end: End date of the pool data timetable period.
    """

    pool_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "poolId",
            "type": "Attribute",
            "required": True,
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ident: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: TimetableInfoTypeType = field(
        default=TimetableInfoTypeType.U,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    begin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    end: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class TripSearchFilterType:
    products: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    gis_products: Optional[str] = field(
        default=None,
        metadata={
            "name": "gisProducts",
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    operators: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    categories: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    attributes: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    sattributes: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    lines: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    line_ids: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineIds",
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    avoid_paths: Optional[str] = field(
        default=None,
        metadata={
            "name": "avoidPaths",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    mobility_profile: Optional[str] = field(
        default=None,
        metadata={
            "name": "mobilityProfile",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    train_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainFilter",
            "type": "Attribute",
            "max_length": 1024,
        },
    )
    group_filter: Optional[str] = field(
        default=None,
        metadata={
            "name": "groupFilter",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    bike_carriage: bool = field(
        default=False,
        metadata={
            "name": "bikeCarriage",
            "type": "Attribute",
        },
    )
    bike_carriage_type: Optional[TripSearchFilterTypeBikeCarriageType] = field(
        default=None,
        metadata={
            "name": "bikeCarriageType",
            "type": "Attribute",
        },
    )
    sleeping_car: bool = field(
        default=False,
        metadata={
            "name": "sleepingCar",
            "type": "Attribute",
        },
    )
    couchette_coach: bool = field(
        default=False,
        metadata={
            "name": "couchetteCoach",
            "type": "Attribute",
        },
    )


@dataclass
class Warnings:
    """
    Warnings.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    warning: List[Warning] = field(
        default_factory=list,
        metadata={
            "name": "Warning",
            "type": "Element",
        },
    )


@dataclass
class CommonResponseType:
    """
    :ivar technical_messages:
    :ivar warnings:
    :ivar server_version: The version of the HAFAS proxy server which
        was used to calculate that result.
    :ivar dialect_version: The version of the response data structure.
    :ivar version: The data version in the HAFAS server which was used
        to calculate that result.
    :ivar plan_rt_ts: The timestamp of the latest real time data update.
    :ivar error_code: If the request fails, then the errorCode is
        filled.
    :ivar error_text: If the request fails, then the errorText is
        filled.
    :ivar request_id: Request ID provided by the caller or generated if
        not present in the request.
    """

    technical_messages: Optional[TechnicalMessages] = field(
        default=None,
        metadata={
            "name": "TechnicalMessages",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    warnings: Optional[Warnings] = field(
        default=None,
        metadata={
            "name": "Warnings",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    server_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "serverVersion",
            "type": "Attribute",
        },
    )
    dialect_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "dialectVersion",
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    plan_rt_ts: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "planRtTs",
            "type": "Attribute",
        },
    )
    error_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorCode",
            "type": "Attribute",
        },
    )
    error_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorText",
            "type": "Attribute",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestId",
            "type": "Attribute",
        },
    )


@dataclass
class ExternalContentType:
    """
    Data type for external use.

    :ivar content: Base64 encoded content string
    :ivar icon: Icon for the content to display.
    :ivar provider: Contains the ID of the provider
    :ivar provider_name: Contains the ID of the provider
    :ivar text: Label to be displayed
    :ivar content_type: Type to identify, how the content is supposed to
        be interpreted
    """

    content: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    provider: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    provider_name: Optional[object] = field(
        default=None,
        metadata={
            "name": "providerName",
            "type": "Attribute",
        },
    )
    text: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[object] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
        },
    )


@dataclass
class Location:
    """
    :ivar note: Note to be displayed
    :ivar id: Contains the ID of the stop/station.
    :ivar ext_id: Contains the external ID of the stop/station.
    :ivar name:
    :ivar lon: The WGS84 longitude of the geographical position of the
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of the
        stop/station
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar type_value: The attribute type specifies the type of location.
        Valid values are ADR (address), POI (point of interest), CRD
        (coordinate), MCP (mode change point) or HL (hailing point).
    """

    note: List[LocationNote] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 512,
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[LocationType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass
class LocationNotes:
    """
    Contains a list of notes to be displayed for this location.

    :ivar location_note: Note to be displayed
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    location_note: List[LocationNote] = field(
        default_factory=list,
        metadata={
            "name": "LocationNote",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class MapLayerType:
    """
    Map.

    :ivar extend: The rectangle map tile having lower left coord(x,y)
        and upper right coord(x,y)
    :ivar initial_bounding_box: Initial rectangle map tile having lower
        left coord(x,y) and upper right coord(x,y)
    :ivar subdomain: list of subdomain-identifiers
    :ivar id: ID
    :ivar url: The URL, from where the map tile will be fetched.
    :ivar zoom_min: Minimum zoom level allowed.
    :ivar zoom_max: Maximum zoom level allowed.
    :ivar opacity: The opacity of a tile in percent. (0=transparent,
        100=opaque).
    :ivar type_value: Type of the map layer.
    :ivar projection: Projectiontype of the tile schema. e.g. Z_X_Y,
        EXTENDS, BBOX etc..
    :ivar attribute: Copyright text for map matelrials (Multi language
        supported)
    :ivar label: Label to display (Multi language supported)
    :ivar show: Show map layer
    :ivar selectable: Map layer is selectable
    """

    extend: Optional[Rect] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    initial_bounding_box: Optional[Rect] = field(
        default=None,
        metadata={
            "name": "initialBoundingBox",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    subdomain: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    zoom_min: int = field(
        default=-1,
        metadata={
            "name": "zoomMin",
            "type": "Attribute",
        },
    )
    zoom_max: int = field(
        default=-1,
        metadata={
            "name": "zoomMax",
            "type": "Attribute",
        },
    )
    opacity: int = field(
        default=100,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    projection: Optional[MapLayerTypeProjection] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    attribute: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    show: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    selectable: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MessageRegionType:
    """
    :ivar name: Name of the region.
    :ivar id: ID of the region.
    :ivar polyline: Polylines describing the region.
    :ivar polyline_group: Polyline groups describing the region.
    :ivar icon_coordinate: Geoposition to draw an icon at
    :ivar ring: A ring describing the geo region affected by this
        message.
    :ivar message_ref: Reference to releated Message@id
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline: List[Polyline] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "polylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    icon_coordinate: Optional[Coordinate] = field(
        default=None,
        metadata={
            "name": "iconCoordinate",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    ring: Optional[Ring] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    message_ref: List[int] = field(
        default_factory=list,
        metadata={
            "name": "messageRef",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class Notes:
    """
    Contains a text with notes to be displayed for this leg, like attributes or
    footnotes.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    note: List[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ProductStatusType:
    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    rt_icon: Optional[IconType] = field(
        default=None,
        metadata={
            "name": "rtIcon",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    code: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    txt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class WeatherInformationType:
    """
    :ivar icon: Weather icon.
    :ivar type_value: Type of weather
    :ivar date: Date, that the weather information is valid for (whole
        day approximation if no time is given). Date in format YYYY-MM-
        DD.
    :ivar time: Time, that the weather information is valid for (on the
        specified date). Time in format hh:mm[:ss]
    :ivar temp: Temperature string including unit as delivered by the
        external weather API
    :ivar text: Short description of the weather (by weather provider)
    :ivar summary: Summary text for the weather
    """

    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    type_value: Optional[WeatherType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    temp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    summary: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AvoidType:
    location: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    status: Optional[AvoidStatusType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    products: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class CoordLocation:
    """The element CoordLocation specifies a coordinate based location in a result
    of a location request.

    It contains an output name, latitude, longitude and a type (address
    or point of interest). The coordinates and the name can be used as
    origin or destination parameters to perform a trip request.

    :ivar location_notes: Contains a list of notes to be displayed for
        this location, like attributes or footnotes.
    :ivar links:
    :ivar icon:
    :ivar child_location: List of child locations. In case of an MCP,
        child locations might be vehicles.
    :ivar weather_information: Weather information for the given
        location - This is a list to support multiple information for
        one day or a 10-day-forecast or else. In the trivial case where
        the weather is requested for a specific point in time, this will
        only contain a single element.
    :ivar id: This optional ID can either be used as originId or destId
        to perform a trip request.
    :ivar ext_id: This ID defines an alternative ID for this stop
        location and can not be used to perform further requests.
    :ivar name: Contains the output name of the address or point of
        interest
    :ivar description: Additional description of location, e.g. address
    :ivar type_value: The attribute type specifies the type of location.
        Valid values are ADR (address), POI (point of interest), CRD
        (coordinate), MCP (mode change point) or HL (hailing point).
    :ivar lon: The WGS84 longitude of the geographical position of the
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of the
        stop/station.
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar dist: This value specifies the distance to the given
        coordinate if called by a nearby search request.
    :ivar refinable: True, if the stop is not resolved fully and could
        be refined.
    :ivar match_value: A percentage value [0, 100] indicating how well
        the name of the given location matches the input location name.
        This attribute is only available in the location.name response
    """

    location_notes: Optional[LocationNotes] = field(
        default=None,
        metadata={
            "name": "LocationNotes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    links: List[ResourceLinks] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    child_location: List["CoordLocation"] = field(
        default_factory=list,
        metadata={
            "name": "childLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    weather_information: List[WeatherInformationType] = field(
        default_factory=list,
        metadata={
            "name": "weatherInformation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[CoordLocationType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refinable: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    match_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "matchValue",
            "type": "Attribute",
        },
    )


@dataclass
class Error(CommonResponseType):
    """
    This element represents the response in case of any error.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"


@dataclass
class LocationPreselectionRequest:
    """
    :ivar reference_location: Reference location that serves as '1' in
        the requested 1:n or n:1
    :ivar gis_profile:
    :ivar mode: Controls which data the service will return in the
        response
    :ivar strategy: Controls which strategy, 1:n or n:1, should be used
        when preselecting locations and routing their edges
    :ivar datetime: Date and time of departure or arrival.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    reference_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "referenceLocation",
            "type": "Element",
            "required": True,
        },
    )
    gis_profile: List[GisProfile] = field(
        default_factory=list,
        metadata={
            "name": "gisProfile",
            "type": "Element",
        },
    )
    mode: LocationPreselectionModeType = field(
        default=LocationPreselectionModeType.ESTIMATE,
        metadata={
            "type": "Attribute",
        },
    )
    strategy: LocationPreselectionStrategyType = field(
        default=LocationPreselectionStrategyType.ONE_TO_N_SELECTION,
        metadata={
            "type": "Attribute",
        },
    )
    datetime: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MapInfoType:
    """
    Map info structure.
    """

    base_map: List[MapLayerType] = field(
        default_factory=list,
        metadata={
            "name": "BaseMap",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    overlay_map: List[MapLayerType] = field(
        default_factory=list,
        metadata={
            "name": "OverlayMap",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class OriginDestType:
    """
    :ivar notes: Contains a list of notes to be displayed for this
        location, like attributes or footnotes.
    :ivar mcp_data: Contains a list of key value pairs describing the
        mode change point data. Only available if @mcp equals to true.
    :ivar message:
    :ivar alt_id:
    :ivar main_mast_alt_id:
    :ivar occupancy:
    :ivar platform:
    :ivar rt_platform:
    :ivar weather_information: Weather information for the given
        location - This is a list to support multiple information for
        one day or a 10-day-forecast or else. In the trivial case where
        the weather is requested for a specific point in time, this will
        only contain a single element.
    :ivar name: Contains the name of the location.
    :ivar description: Additional description of location, e.g. address
    :ivar type_value: The attribute type specifies the type of location.
        Valid values are ST (stop/station), ADR (address), POI (point of
        interest), CRD (coordinate), MCP (mode change point) or HL
        (hailing point).
    :ivar id: ID of this stop
    :ivar ext_id: External ID of this stop
    :ivar lon: The WGS84 longitude of the geographical position.
    :ivar lat: The WGS84 latitude of the geographical position.
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar route_idx: Route index of a stop/station. Can be used as a
        reference of the stop/station in a journeyDetail response.
    :ivar prognosis_type: Prognosis type of date and time.
    :ivar time: Time in format hh:mm[:ss].
    :ivar date: Date in format YYYY-MM-DD.
    :ivar tz: Time zone information in the format +/- minutes
    :ivar scheduled_time_changed: Scheduled time changed.
    :ivar track: Track information, if available.
    :ivar track_hidden: True if track information is hidden by data.
    :ivar rt_time: Realtime time in format hh:mm[:ss] if available.
    :ivar rt_date: Realtime date in format YYYY-MM-DD, if available.
    :ivar rt_tz: Realtime time zone information in the format +/-
        minutes, if available.
    :ivar rt_track: Realtime track information, if available.
    :ivar rt_track_hidden: True if track information is hidden by
        realtime data.
    :ivar has_main_mast: True if this stop belongs to a main mast.
    :ivar main_mast_id: ID of the main mast this stop belongs to.
    :ivar main_mast_ext_id: External ID of the main mast this stop
        belongs to.
    :ivar main_mast_lon: The WGS84 longitude of the geographical
        position of the main mast this stop/station.
    :ivar main_mast_lat: The WGS84 latitude of the geographical position
        of the main mast this stop/station.
    :ivar main_mast_alt: The altitude of the geographical position of
        the main mast this stop/station.
    :ivar alighting: True if alighting is allowed by scheduled data
    :ivar boarding: True if boarding is allowed by scheduled data
    :ivar rt_alighting: True if alighting is allowed by realtime data
    :ivar rt_boarding: True if boarding is allowed by realtime data
    :ivar cancelled: Will be true if arrival or departure or both at
        this stop is cancelled
    :ivar cancelled_departure: Will be true if departure at this stop is
        cancelled
    :ivar cancelled_arrival: Will be true if arrival at this stop is
        cancelled
    :ivar uncertain_delay: The journey stopped or is waiting and the
        stop has an uncertain delay.
    :ivar additional: Will be true if this stop is an additional stop
    :ivar is_border_stop: Will be true if this stop is a border stop
    :ivar is_turning_point: Will be true if this stop is a turning point
    :ivar hide: If true, hide times and track information.
    :ivar entry: True, if the stop is an entry point.
    :ivar mcp: True if this stop is a mode change point, e.g. car
        sharing station, charging station etc.
    :ivar train_composition_marker: Indicates an external train
        composition is available.
    :ivar rt_cncl_data_source_type: Realtime data source that the stop
        cancellation originates from
    :ivar ps_ctx_arrive_earlier: Provides a context that may be used in
        service PartialSearch to increase the time for interchange
        between the previous journey arrival stop and the following
        journey departure stop by searching a trip that will lead to an
        earlier arrival time for the previous journey while keeping the
        departure time for the following journey(s) constant.
    :ivar ps_ctx_depart_later: Provides a context that may be used in
        service PartialSearch to increase the time for interchange
        between the previous journey arrival stop and the following
        journey departure stop by searching a trip that will lead to a
        later departure time for the following journey while keeping the
        arrival time for the previous journey(s) constant.
    """

    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    mcp_data: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "mcpData",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    message: List["Message"] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    main_mast_alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "mainMastAltId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    rt_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "rtPlatform",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    weather_information: List[WeatherInformationType] = field(
        default_factory=list,
        metadata={
            "name": "weatherInformation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[OriginDestTypeType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdx",
            "type": "Attribute",
        },
    )
    prognosis_type: Optional[PrognosisType] = field(
        default=None,
        metadata={
            "name": "prognosisType",
            "type": "Attribute",
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tz: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    scheduled_time_changed: bool = field(
        default=False,
        metadata={
            "name": "scheduledTimeChanged",
            "type": "Attribute",
        },
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track_hidden: bool = field(
        default=False,
        metadata={
            "name": "trackHidden",
            "type": "Attribute",
        },
    )
    rt_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTime",
            "type": "Attribute",
        },
    )
    rt_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDate",
            "type": "Attribute",
        },
    )
    rt_tz: int = field(
        default=0,
        metadata={
            "name": "rtTz",
            "type": "Attribute",
        },
    )
    rt_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTrack",
            "type": "Attribute",
        },
    )
    rt_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "rtTrackHidden",
            "type": "Attribute",
        },
    )
    has_main_mast: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasMainMast",
            "type": "Attribute",
        },
    )
    main_mast_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastId",
            "type": "Attribute",
        },
    )
    main_mast_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastExtId",
            "type": "Attribute",
        },
    )
    main_mast_lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLon",
            "type": "Attribute",
        },
    )
    main_mast_lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLat",
            "type": "Attribute",
        },
    )
    main_mast_alt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mainMastAlt",
            "type": "Attribute",
        },
    )
    alighting: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    boarding: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    rt_alighting: Optional[bool] = field(
        default=None,
        metadata={
            "name": "rtAlighting",
            "type": "Attribute",
        },
    )
    rt_boarding: Optional[bool] = field(
        default=None,
        metadata={
            "name": "rtBoarding",
            "type": "Attribute",
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    cancelled_departure: bool = field(
        default=False,
        metadata={
            "name": "cancelledDeparture",
            "type": "Attribute",
        },
    )
    cancelled_arrival: bool = field(
        default=False,
        metadata={
            "name": "cancelledArrival",
            "type": "Attribute",
        },
    )
    uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "uncertainDelay",
            "type": "Attribute",
        },
    )
    additional: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    is_border_stop: bool = field(
        default=False,
        metadata={
            "name": "isBorderStop",
            "type": "Attribute",
        },
    )
    is_turning_point: bool = field(
        default=False,
        metadata={
            "name": "isTurningPoint",
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    entry: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mcp: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    train_composition_marker: Optional[int] = field(
        default=None,
        metadata={
            "name": "trainCompositionMarker",
            "type": "Attribute",
        },
    )
    rt_cncl_data_source_type: Optional[RealtimeDataSourceType] = field(
        default=None,
        metadata={
            "name": "rtCnclDataSourceType",
            "type": "Attribute",
        },
    )
    ps_ctx_arrive_earlier: Optional[str] = field(
        default=None,
        metadata={
            "name": "psCtxArriveEarlier",
            "type": "Attribute",
        },
    )
    ps_ctx_depart_later: Optional[str] = field(
        default=None,
        metadata={
            "name": "psCtxDepartLater",
            "type": "Attribute",
        },
    )


@dataclass
class PartialSearchSegmentLocation(Location):
    """
    :ivar date: Corresponding date for segment in format YYYY-MM-DD. If
        not set, the first location in the reconstruction will be used
        that matches the location.
    :ivar time: Corresponding time for segment in format hh:mm[:ss]. If
        not set, the first location in the reconstruction will be used
        that matches the location.
    :ivar suppl_chg_time: Supplementary change time at station to be
        considered as a minimum.
    """

    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    suppl_chg_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "supplChgTime",
            "type": "Attribute",
        },
    )


@dataclass
class PreselectionNodeType:
    """
    :ivar id: Unique ID that will be attached to all sections that
        resulted from this node.
    :ivar location: Location for the preselected node that will serve as
        transition point
    :ivar preselection_edge: List of (long) edges to/from this node,
        each being an option / alternative
    """

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    location: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    preselection_edge: List[PreselectionEdgeType] = field(
        default_factory=list,
        metadata={
            "name": "PreselectionEdge",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class ProviderType:
    """
    :ivar external_content:
    :ivar id: Provider ID.
    :ivar name: Name of provider.
    :ivar region: Region this provider is active/responsible.
    """

    external_content: Optional[ExternalContentType] = field(
        default=None,
        metadata={
            "name": "externalContent",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    region: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ReconstructionConvertResponse(CommonResponseType):
    """
    Returns a list of converted reconstruction contexts.

    :ivar ctx: Converted reconstruction context.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ctx: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ReconstructionSectionDataType:
    """
    Information regarding Sections of a Journey.

    :ivar departure: Start location of the section - departure location.
    :ivar arrival: End location of the section - arrival location.
    :ivar type_value: Mode of transportation.
    :ivar departure_time: Departure time based on schedule.
    :ivar departure_time_rt: Actual departure time based.
    :ivar arrival_time: Arrival time based on schedule.
    :ivar arrival_time_rt: Actual arrival time.
    :ivar train_name: Name of the product.
    :ivar train_number: External train number.
    :ivar train_category: Product category.
    """

    departure: Optional[Location] = field(
        default=None,
        metadata={
            "name": "Departure",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    arrival: Optional[Location] = field(
        default=None,
        metadata={
            "name": "Arrival",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    type_value: Optional[ReconstructionSectionType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    departure_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "departureTime",
            "type": "Attribute",
        },
    )
    departure_time_rt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "departureTimeRt",
            "type": "Attribute",
        },
    )
    arrival_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "arrivalTime",
            "type": "Attribute",
        },
    )
    arrival_time_rt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "arrivalTimeRt",
            "type": "Attribute",
        },
    )
    train_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainName",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    train_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainNumber",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    train_category: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainCategory",
            "type": "Attribute",
            "max_length": 512,
        },
    )


@dataclass
class StopType:
    """
    The element Stop contains the name of the stop/station, the route index, the
    latitude, the longitude, the departure time and date, the arrival time and
    date, the track, the realtime departure time and date, the realtime arrival
    time and date and the realtime track.

    :ivar notes: Contains a list of notes to be displayed for this
        location, like attributes or footnotes.
    :ivar alt_id:
    :ivar main_mast_alt_id:
    :ivar occupancy:
    :ivar arr_platform:
    :ivar rt_arr_platform:
    :ivar dep_platform:
    :ivar rt_dep_platform:
    :ivar weather_information: Weather information for the given
        location - This is a list to support multiple information for
        one day or a 10-day-forecast or else. In the trivial case where
        the weather is requested for a specific point in time, this will
        only contain a single element.
    :ivar name: Contains the name of the stop/station.
    :ivar description: Additional description of location, e.g. address
    :ivar id: Contains the ID of the stop/station.
    :ivar ext_id: Contains the external ID of the stop/station.
    :ivar route_idx: Route index of a stop/station. Usually starting
        from 0 and incrementing by 1. If the route index value jumps, it
        is most likely that the journey was rerouted.
    :ivar lon: The WGS84 longitude of the geographical position of the
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of the
        stop/station
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar arr_prognosis_type: Prognosis type of arrival date and time.
    :ivar dep_prognosis_type: Prognosis type of departure date and time.
    :ivar dep_time: Departure time in format hh:mm[:ss], if available.
    :ivar dep_date: Departure date in format YYYY-MM-DD, if available.
    :ivar dep_tz: Departure time zone information in the format +/-
        minutes
    :ivar scheduled_dep_time_changed: Scheduled departure time changed.
    :ivar arr_time: Arrival time in format hh:mm[:ss], if available.
    :ivar arr_date: Arrival date in format YYYY-MM-DD, if available.
    :ivar arr_tz: Arrival time zone information in the format +/-
        minutes
    :ivar scheduled_arr_time_changed: Scheduled arrival time changed.
    :ivar passing_time: Passing time in format hh:mm[:ss], if available.
    :ivar passing_date: Passing date in format YYYY-MM-DD, if available.
    :ivar passing_tz: Passing time zone information in the format +/-
        minutes
    :ivar arr_track: Arrival track information, if available.
    :ivar arr_track_hidden: True if arrival track information is hidden
        by data.
    :ivar dep_track: Departure track information, if available.
    :ivar dep_track_hidden: True if departure track information is
        hidden by data.
    :ivar rt_dep_time: Realtime departure time in format hh:mm[:ss] if
        available.
    :ivar rt_dep_date: Realtime departure date in format YYYY-MM-DD, if
        available.
    :ivar rt_dep_tz: Realtime departure time zone information in the
        format +/- minutes, if available.
    :ivar rt_arr_time: Realtime arrival time in format hh:mm[:ss] if
        available.
    :ivar rt_arr_date: Realtime arrival date in format YYYY-MM-DD, if
        available.
    :ivar rt_arr_tz: Realtime arrival time zone information in the
        format +/- minutes, if available.
    :ivar rt_arr_track: Realtime arrival track information, if
        available.
    :ivar rt_arr_track_hidden: True if arrival track information is
        hidden by realtime data.
    :ivar rt_dep_track: Realtime departure track information, if
        available.
    :ivar rt_dep_track_hidden: True if track information is hidden by
        realtime data.
    :ivar rt_passing_time: Realtime passing time in format hh:mm[:ss],
        if available.
    :ivar rt_passing_date: Realtime passing date in format YYYY-MM-DD,
        if available.
    :ivar rt_passing_tz: Realtime passing time zone information in the
        format +/- minutes, if available.
    :ivar cancelled: Will be true if arrival or departure or both at
        this stop is cancelled
    :ivar cancelled_departure: Will be true if departure at this stop is
        cancelled
    :ivar cancelled_arrival: Will be true if arrival at this stop is
        cancelled
    :ivar has_main_mast: True if this stop belongs to a main mast.
    :ivar main_mast_id: ID of the main mast this stop belongs to.
    :ivar main_mast_ext_id: External ID of the main mast this stop
        belongs to.
    :ivar main_mast_lon: The WGS84 longitude of the geographical
        position of the main mast this stop/station.
    :ivar main_mast_lat: The WGS84 latitude of the geographical position
        of the main mast this stop/station.
    :ivar main_mast_alt: The altitude of the geographical position of
        the main mast this stop/station.
    :ivar alighting: True if alighting is allowed by scheduled data
    :ivar boarding: True if boarding is allowed by scheduled data
    :ivar rt_alighting: True if alighting is allowed by realtime data
    :ivar rt_boarding: True if boarding is allowed by realtime data
    :ivar additional: Will be true if this stop is an additional stop
    :ivar is_border_stop: Will be true if this stop is a border stop
    :ivar is_turning_point: Will be true if this stop is a turning point
    :ivar arr_hide: If true, hide arrival times and track information.
    :ivar dep_hide: If true, hide departure times and track information.
    :ivar dep_dir: Direction information.
    :ivar entry: True, if the stop is an entry point.
    :ivar rt_cncl_data_source_type: Realtime data source that the stop
        cancellation originates from
    :ivar arr_uncertain_delay: The journey stopped or is waiting and the
        stop has an uncertain delay.
    :ivar dep_uncertain_delay: The journey stopped or is waiting and the
        stop has an uncertain delay.
    """

    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    main_mast_alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "mainMastAltId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    arr_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "arrPlatform",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    rt_arr_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "rtArrPlatform",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    dep_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "depPlatform",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    rt_dep_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "rtDepPlatform",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    weather_information: List[WeatherInformationType] = field(
        default_factory=list,
        metadata={
            "name": "weatherInformation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
            "required": True,
        },
    )
    route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdx",
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    arr_prognosis_type: Optional[PrognosisType] = field(
        default=None,
        metadata={
            "name": "arrPrognosisType",
            "type": "Attribute",
        },
    )
    dep_prognosis_type: Optional[PrognosisType] = field(
        default=None,
        metadata={
            "name": "depPrognosisType",
            "type": "Attribute",
        },
    )
    dep_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "depTime",
            "type": "Attribute",
        },
    )
    dep_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "depDate",
            "type": "Attribute",
        },
    )
    dep_tz: int = field(
        default=0,
        metadata={
            "name": "depTz",
            "type": "Attribute",
        },
    )
    scheduled_dep_time_changed: bool = field(
        default=False,
        metadata={
            "name": "scheduledDepTimeChanged",
            "type": "Attribute",
        },
    )
    arr_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "arrTime",
            "type": "Attribute",
        },
    )
    arr_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "arrDate",
            "type": "Attribute",
        },
    )
    arr_tz: int = field(
        default=0,
        metadata={
            "name": "arrTz",
            "type": "Attribute",
        },
    )
    scheduled_arr_time_changed: bool = field(
        default=False,
        metadata={
            "name": "scheduledArrTimeChanged",
            "type": "Attribute",
        },
    )
    passing_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "passingTime",
            "type": "Attribute",
        },
    )
    passing_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "passingDate",
            "type": "Attribute",
        },
    )
    passing_tz: int = field(
        default=0,
        metadata={
            "name": "passingTz",
            "type": "Attribute",
        },
    )
    arr_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "arrTrack",
            "type": "Attribute",
        },
    )
    arr_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "arrTrackHidden",
            "type": "Attribute",
        },
    )
    dep_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "depTrack",
            "type": "Attribute",
        },
    )
    dep_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "depTrackHidden",
            "type": "Attribute",
        },
    )
    rt_dep_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDepTime",
            "type": "Attribute",
        },
    )
    rt_dep_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDepDate",
            "type": "Attribute",
        },
    )
    rt_dep_tz: int = field(
        default=0,
        metadata={
            "name": "rtDepTz",
            "type": "Attribute",
        },
    )
    rt_arr_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtArrTime",
            "type": "Attribute",
        },
    )
    rt_arr_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtArrDate",
            "type": "Attribute",
        },
    )
    rt_arr_tz: int = field(
        default=0,
        metadata={
            "name": "rtArrTz",
            "type": "Attribute",
        },
    )
    rt_arr_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtArrTrack",
            "type": "Attribute",
        },
    )
    rt_arr_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "rtArrTrackHidden",
            "type": "Attribute",
        },
    )
    rt_dep_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDepTrack",
            "type": "Attribute",
        },
    )
    rt_dep_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "rtDepTrackHidden",
            "type": "Attribute",
        },
    )
    rt_passing_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtPassingTime",
            "type": "Attribute",
        },
    )
    rt_passing_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtPassingDate",
            "type": "Attribute",
        },
    )
    rt_passing_tz: int = field(
        default=0,
        metadata={
            "name": "rtPassingTz",
            "type": "Attribute",
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    cancelled_departure: bool = field(
        default=False,
        metadata={
            "name": "cancelledDeparture",
            "type": "Attribute",
        },
    )
    cancelled_arrival: bool = field(
        default=False,
        metadata={
            "name": "cancelledArrival",
            "type": "Attribute",
        },
    )
    has_main_mast: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasMainMast",
            "type": "Attribute",
        },
    )
    main_mast_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastId",
            "type": "Attribute",
        },
    )
    main_mast_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastExtId",
            "type": "Attribute",
        },
    )
    main_mast_lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLon",
            "type": "Attribute",
        },
    )
    main_mast_lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLat",
            "type": "Attribute",
        },
    )
    main_mast_alt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mainMastAlt",
            "type": "Attribute",
        },
    )
    alighting: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    boarding: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    rt_alighting: Optional[bool] = field(
        default=None,
        metadata={
            "name": "rtAlighting",
            "type": "Attribute",
        },
    )
    rt_boarding: Optional[bool] = field(
        default=None,
        metadata={
            "name": "rtBoarding",
            "type": "Attribute",
        },
    )
    additional: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    is_border_stop: bool = field(
        default=False,
        metadata={
            "name": "isBorderStop",
            "type": "Attribute",
        },
    )
    is_turning_point: bool = field(
        default=False,
        metadata={
            "name": "isTurningPoint",
            "type": "Attribute",
        },
    )
    arr_hide: bool = field(
        default=False,
        metadata={
            "name": "arrHide",
            "type": "Attribute",
        },
    )
    dep_hide: bool = field(
        default=False,
        metadata={
            "name": "depHide",
            "type": "Attribute",
        },
    )
    dep_dir: Optional[str] = field(
        default=None,
        metadata={
            "name": "depDir",
            "type": "Attribute",
        },
    )
    entry: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rt_cncl_data_source_type: Optional[RealtimeDataSourceType] = field(
        default=None,
        metadata={
            "name": "rtCnclDataSourceType",
            "type": "Attribute",
        },
    )
    arr_uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "arrUncertainDelay",
            "type": "Attribute",
        },
    )
    dep_uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "depUncertainDelay",
            "type": "Attribute",
        },
    )


@dataclass
class TariffValidation(CommonResponseType):
    """
    The location contains details for a stop/station or POI.

    :ivar valid: Returns true in case of a valid tariff.
    :ivar reason: Text/Code explaining cause for invalidation.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    valid: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class TimetableInfoList(CommonResponseType):
    """The time table info list contains entries for each pool of the connected
    HAFAS server.

    Each entry has a date and time attribute representing the point in
    time the pool was generated. The attribute ident identifies that
    specific pool. The list itself carries the begin and end date of the
    planning period as attributes.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    timetable_info: List[TimetableInfoType] = field(
        default_factory=list,
        metadata={
            "name": "TimetableInfo",
            "type": "Element",
        },
    )
    begin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    end: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class TrackPoint:
    """
    :ivar location: The tracked location (coordinate, external id,
        etc.).
    :ivar probability: Probability with values ranging from -1 to 100.
        -1 signifies an unknown probability.
    :ivar timestamp: Date and time of the tracked coordinate.
    :ivar se_id: Tracking specific id (specific to the used algorithm).
    :ivar source: Source of the tracked coordinate.
    :ivar accuracy: Accuracy of the tracked coordinate. Smaller values
        mean higher accuracy.
    :ivar speed: Speed in meters per second.
    :ivar direction: Direction corresponding to 0 to 360 degrees
        starting at north and increasing clockwise.
    :ivar train_name:
    :ivar line_name:
    :ivar product: Product mask.
    """

    location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    probability: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "Probability",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    se_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "seId",
            "type": "Attribute",
        },
    )
    source: Optional[TrackPoinSourceType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    accuracy: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    speed: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    direction: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    train_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainName",
            "type": "Attribute",
        },
    )
    line_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineName",
            "type": "Attribute",
        },
    )
    product: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class TrackSectionData:
    """
    :ivar departure: Start location of the section - departure location.
    :ivar arrival: End location of the section - arrival location.
    :ivar type_value: Mode of transportation.
    :ivar match_time_span_begin: Start of the match.
    :ivar match_time_span_end: End of the match.
    :ivar departure_time: Departure time based on schedule.
    :ivar departure_time_rt: Actual departure time based.
    :ivar arrival_time: Arrival time based on schedule.
    :ivar arrival_time_rt: Actual arrival time.
    :ivar train_name:
    :ivar train_number:
    :ivar train_category:
    """

    departure: Optional[Location] = field(
        default=None,
        metadata={
            "name": "Departure",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    arrival: Optional[Location] = field(
        default=None,
        metadata={
            "name": "Arrival",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    type_value: Optional[ReconstructionSectionType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    match_time_span_begin: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "matchTimeSpanBegin",
            "type": "Attribute",
        },
    )
    match_time_span_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "matchTimeSpanEnd",
            "type": "Attribute",
        },
    )
    departure_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "departureTime",
            "type": "Attribute",
        },
    )
    departure_time_rt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "departureTimeRt",
            "type": "Attribute",
        },
    )
    arrival_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "arrivalTime",
            "type": "Attribute",
        },
    )
    arrival_time_rt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "arrivalTimeRt",
            "type": "Attribute",
        },
    )
    train_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainName",
            "type": "Attribute",
        },
    )
    train_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainNumber",
            "type": "Attribute",
        },
    )
    train_category: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainCategory",
            "type": "Attribute",
        },
    )


@dataclass
class ViaType:
    location: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    wait_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "waitTime",
            "type": "Attribute",
        },
    )
    status: Optional[ViaStatusType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    products: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    attributes: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 512,
        },
    )
    direct: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    sleeping_car: bool = field(
        default=False,
        metadata={
            "name": "sleepingCar",
            "type": "Attribute",
        },
    )
    couchette_coach: bool = field(
        default=False,
        metadata={
            "name": "couchetteCoach",
            "type": "Attribute",
        },
    )


@dataclass
class Ticket:
    """
    :ivar param:
    :ivar external_content:
    :ivar name:
    :ivar desc:
    :ivar price:
    :ivar cur:
    :ivar shp_ctx:
    :ivar from_leg: Deprecated, use fromLegId. First leg this ticket is
        valid for.
    :ivar to_leg: Deprecated, use toLegId. Last leg this ticket is valid
        for.
    :ivar from_leg_id: First leg ID this ticket is valid for.
    :ivar to_leg_id: Last leg ID this ticket is valid for.
    """

    class Meta:
        name = "ticket"
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    param: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    external_content: Optional[ExternalContentType] = field(
        default=None,
        metadata={
            "name": "externalContent",
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    price: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    cur: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shp_ctx: Optional[str] = field(
        default=None,
        metadata={
            "name": "shpCtx",
            "type": "Attribute",
        },
    )
    from_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "fromLeg",
            "type": "Attribute",
        },
    )
    to_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "toLeg",
            "type": "Attribute",
        },
    )
    from_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fromLegId",
            "type": "Attribute",
        },
    )
    to_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "toLegId",
            "type": "Attribute",
        },
    )


@dataclass
class Destination(OriginDestType):
    """
    Destination of a leg including location name, location type, location route
    index (if available), arrival time and date, realtime arrival time (if
    available), track and realtime track (if available)
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"


@dataclass
class GeoFeatureType:
    """
    :ivar provider: The provider of the GeoFeature.
    :ivar icon: Icon that illustrates the GeoFeature.
    :ivar coordinate: A list of coordinates relating to the GeoFeature.
    :ivar lines: A list of polylines relating to the GeoFeature.
    :ivar geo_data: A list of polylines relating to the GeoFeature.
    :ivar validity: List of date/time intervals in which the GeoFeature
        is valid.
    :ivar note: Note for GeoFeature.
    :ivar id: The internal id of the GeoFeature.
    :ivar ext_id: The external if of the GeoFeature.
    :ivar type_value: The type of the GeoFeature
    :ivar sub_type: The subtype of the GeoFeature
    :ivar title: The title describing the GeoFeature
    """

    provider: Optional[ProviderType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    coordinate: List[Coordinate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    lines: List[Polyline] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    geo_data: List[GeoDataType] = field(
        default_factory=list,
        metadata={
            "name": "geoData",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    validity: List[DateTimeIntervalType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    note: List[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ext_id: Optional[object] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    type_value: Optional[GeoFeatureTypeType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    sub_type: Optional[object] = field(
        default=None,
        metadata={
            "name": "subType",
            "type": "Attribute",
        },
    )
    title: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class JourneyPathType:
    """
    :ivar journey_path_item: Single item to represent a journey path
        element.
    :ivar location: Locations refered along the journey path.
    :ivar polyline_group: Polyline representing this segment.
    """

    journey_path_item: List[JourneyPathItemType] = field(
        default_factory=list,
        metadata={
            "name": "JourneyPathItem",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )
    location: List[StopType] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "PolylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class MessageEdgeType:
    """
    :ivar s_stop: Start stop of this edge.
    :ivar e_stop: End stop of this edge.
    :ivar polyline: Polylines describing the route graph
    :ivar polyline_group: Polyline groups describing the route graph
    :ivar icon_coordinate: Geoposition to draw an icon at
    :ivar message_ref: Reference to releated Message@id
    :ivar direction: Direction on the egde the message is valid for: 0:
        unknown; 1: in direction of egde; 2: in oposite direction of
        edge; 3: both directions
    """

    s_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "sStop",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    e_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "eStop",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline: List[Polyline] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "polylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    icon_coordinate: Optional[Coordinate] = field(
        default=None,
        metadata={
            "name": "iconCoordinate",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    message_ref: List[int] = field(
        default_factory=list,
        metadata={
            "name": "messageRef",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    direction: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MessageEventType:
    """
    :ivar s_stop: Start stop of this event.
    :ivar e_stop: End stop of this event.
    :ivar section_num: Section numbers this event is valid for.
    :ivar s_time: Event period beginning time in format hh:mm[:ss]
    :ivar s_date: Event period beginning date in format YYYY-MM-DD.
    :ivar e_time: Event period ending time in format hh:mm[:ss]
    :ivar e_date: Event period ending date in format YYYY-MM-DD.
    :ivar current: Event is valid currently.
    """

    s_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "sStop",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    e_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "eStop",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    section_num: List[str] = field(
        default_factory=list,
        metadata={
            "name": "sectionNum",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    s_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "sTime",
            "type": "Attribute",
        },
    )
    s_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDate",
            "type": "Attribute",
        },
    )
    e_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "eTime",
            "type": "Attribute",
        },
    )
    e_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "eDate",
            "type": "Attribute",
        },
    )
    current: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Origin(OriginDestType):
    """
    Origin of a leg including location name, location type, location route index
    (if available), departure time and date, realtime departure (if available),
    track and realtime track (if available).
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"


@dataclass
class ParallelJourneyRefType:
    """
    Information on parallel journeys.

    :ivar from_location: Combination location.
    :ivar to_location: Separation location.
    :ivar journey_detail_ref: Reference to journey details of this
        journey.
    :ivar type_value: Type of the parallel journey.
    """

    from_location: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "fromLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    to_location: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "toLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey_detail_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "journeyDetailRef",
            "type": "Attribute",
            "max_length": 512,
        },
    )
    type_value: ParallelJourneyType = field(
        default=ParallelJourneyType.UNDEF,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass
class PartialSearchSegmentType:
    """
    :ivar begin_location: Marks the beginning of the segment and refers
        a location from the reconstruction context. Optional:
        Corresponding time for the beginning of the segment. If not set,
        the first location in the reconstruction context will be used
        that matches the beginning location. Optional: Supplementary
        change time at station at the beginning to be considered as a
        minimum.
    :ivar end_location: Marks the end of the segment and refers to a
        location from the reconstruction context. Optional:
        Corresponding time for the end of the segment. If not set, the
        first location in the reconstruction context will be used that
        matches the end location. Optional: Supplementary change time at
        station at the end to be considered as a minimum.
    """

    begin_location: Optional[PartialSearchSegmentLocation] = field(
        default=None,
        metadata={
            "name": "beginLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    end_location: Optional[PartialSearchSegmentLocation] = field(
        default=None,
        metadata={
            "name": "endLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )


@dataclass
class PreselectionType:
    """
    :ivar gis_profile:
    :ivar node: Specifies the preselected nodes that will serve as
        transition points
    """

    gis_profile: Optional[GisProfile] = field(
        default=None,
        metadata={
            "name": "gisProfile",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    node: List[PreselectionNodeType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class ProductType:
    """Product context, provides access to internal data.

    For the product category attributes, their assignments are defined
    in the "zugart" file from the raw Hafas plan data.

    :ivar icon:
    :ivar status:
    :ivar from_location:
    :ivar to_location:
    :ivar operator_info:
    :ivar name: Product name for display. The name might be composed
        from product number, line and/or category. This is customer
        specific. In case of a non public transport product like bike,
        car, taxi or walk, this field is filled with a localized value
        for the specific type. Same for check-in or check-out. Samples:
        - Walk -&gt; Chemin piéton (French), Gå (Danish)... - Transfer
        -&gt; Transfert (French), Gå (Udveksling)... Those localizations
        can be configured in the underlying HAFAS system. In case of a
        sharing provider, this field might be filled with provider name
        if data covers that.
    :ivar internal_name: Internal product name. Not used for display.
        Used e.g. in reconstruction services.
    :ivar add_name: Additional product name. This is customer specific.
    :ivar display_number: Number for display
    :ivar num: Internal product number (e.g. train number)
    :ivar line: Line name if available (e.g. "R10")
    :ivar line_id: External line id for use in further requests
    :ivar cat_out: Product category name as used for display in standard
        form.
    :ivar cat_in: Internal product category name.
    :ivar cat_code: Product category code.
    :ivar cls: Product category in decimal form.
    :ivar cat_out_s: Product category name for display in short form.
    :ivar cat_out_l: Product category name for display in long form.
    :ivar operator_code: Deprecated since 2.31. Use operator.nameS. The
        operator code.
    :ivar operator: Deprecated since 2.31. Use operator.name. The
        operator name.
    :ivar admin: The administration name.
    :ivar route_idx_from: Defines the first stop/station where this name
        is valid. See the Stops list for details of the stop/station.
    :ivar route_idx_to: Defines the last stop/station where this name is
        valid. See the Stops list for details of the stop/station.
    :ivar match_id: The match ID.
    :ivar tar_gr: Tariff group.
    :ivar surcharge: Flag indicating surcharge.
    :ivar out_ctrl: Control flag for train name output.
    :ivar loc_traffic: Flag indicating local traffic.
    :ivar ship_traffic: Flag indicating product relates to shipping
        traffic.
    """

    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    status: Optional[ProductStatusType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    from_location: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "fromLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    to_location: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "toLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    operator_info: Optional[OperatorType] = field(
        default=None,
        metadata={
            "name": "operatorInfo",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    internal_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "internalName",
            "type": "Attribute",
        },
    )
    add_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "addName",
            "type": "Attribute",
        },
    )
    display_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "displayNumber",
            "type": "Attribute",
        },
    )
    num: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    line: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineId",
            "type": "Attribute",
        },
    )
    cat_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "catOut",
            "type": "Attribute",
        },
    )
    cat_in: Optional[str] = field(
        default=None,
        metadata={
            "name": "catIn",
            "type": "Attribute",
        },
    )
    cat_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "catCode",
            "type": "Attribute",
        },
    )
    cls: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cat_out_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "catOutS",
            "type": "Attribute",
        },
    )
    cat_out_l: Optional[str] = field(
        default=None,
        metadata={
            "name": "catOutL",
            "type": "Attribute",
        },
    )
    operator_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "operatorCode",
            "type": "Attribute",
        },
    )
    operator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    admin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx_from: int = field(
        default=-1,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: int = field(
        default=-1,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )
    match_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "matchId",
            "type": "Attribute",
        },
    )
    tar_gr: Optional[str] = field(
        default=None,
        metadata={
            "name": "tarGr",
            "type": "Attribute",
        },
    )
    surcharge: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    out_ctrl: Optional[str] = field(
        default=None,
        metadata={
            "name": "outCtrl",
            "type": "Attribute",
        },
    )
    loc_traffic: Optional[str] = field(
        default=None,
        metadata={
            "name": "locTraffic",
            "type": "Attribute",
        },
    )
    ship_traffic: Optional[str] = field(
        default=None,
        metadata={
            "name": "shipTraffic",
            "type": "Attribute",
        },
    )


@dataclass
class ReconstructionMatchRequest:
    """
    Information regarding Sections of a Journey.

    :ivar section:
    :ivar traveller_profile:
    :ivar use_combined_comparison: Compare based on combined output name
        - false: Compare parameters (category, line, train number)
        individually
    :ivar accept_gaps: Accept an incomplete description of the
        connection (with gaps) i.e. missing walks/transfers
    :ivar flag_all_non_reachable: Should all non-reachable journeys be
        flagged (true), or only the first one encountered?
    :ivar match_cat_strict: Should the category (Gattung) match exactly?
        Only applicable if useCombinedComparison is false
    :ivar match_id_non_blank: Should the train identifier
        (Zugbezeichner) without whitespace match?
    :ivar match_id_strict: Should the train identifier (Zugbezeichner)
        match exactly?
    :ivar match_num_strict: Should the train number (Zugnummer) match
        exactly? Only applicable if useCombinedComparison is false
    :ivar match_rt_type: Should the realtime type that journeys are
        based on (e.g. SOLL, IST, additional, deviation, ...) be
        considered?
    :ivar allow_dummy_sections: Allow a partial reconstruction that will
        not lead to a reconstruction failure if sections are not
        reconstructable. Instead, for theses inconstructable sections,
        dummy sections will be created in the result.
    :ivar enable_rt_full_search: By default, the reconstruction request
        makes one attempt for each journey within the scheduled data.
        However, the scheduled data may not necessarily reflect basic
        realtime properties of the journeys therein. In such a case, one
        may enable a two-step approach which we call "full search", i.e.
        search for matching journeys in the scheduled data in a first
        step. If this fails, then search for matching journeys in the
        realtime data.
    :ivar enable_replacements: If set to true replaces cancelled
        journeys with their replacement journeys if possible.
    :ivar with_journey_boundary_points: Enables/disables the return of
        journey boundary stops at public transport legs.
    :ivar arr_l: Lower deviation in minutes within interval [0, 720]
        indicating "how much earlier than original arrival"
    :ivar arr_u: Upper deviation in minutes within interval [0, 720]
        indicating "how much later than original arrival"
    :ivar dep_l: Lower deviation in minutes within interval [0, 720]
        indicating "how much earlier than original departure"
    :ivar dep_u: Upper deviation in minutes within interval [0, 720]
        indicating "how much later than original departure"
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    section: List[ReconstructionSectionDataType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    traveller_profile: Optional[TravellerProfileType] = field(
        default=None,
        metadata={
            "name": "travellerProfile",
            "type": "Element",
        },
    )
    use_combined_comparison: Optional[bool] = field(
        default=None,
        metadata={
            "name": "useCombinedComparison",
            "type": "Attribute",
        },
    )
    accept_gaps: Optional[bool] = field(
        default=None,
        metadata={
            "name": "acceptGaps",
            "type": "Attribute",
        },
    )
    flag_all_non_reachable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "flagAllNonReachable",
            "type": "Attribute",
        },
    )
    match_cat_strict: Optional[bool] = field(
        default=None,
        metadata={
            "name": "matchCatStrict",
            "type": "Attribute",
        },
    )
    match_id_non_blank: Optional[bool] = field(
        default=None,
        metadata={
            "name": "matchIdNonBlank",
            "type": "Attribute",
        },
    )
    match_id_strict: Optional[bool] = field(
        default=None,
        metadata={
            "name": "matchIdStrict",
            "type": "Attribute",
        },
    )
    match_num_strict: Optional[bool] = field(
        default=None,
        metadata={
            "name": "matchNumStrict",
            "type": "Attribute",
        },
    )
    match_rt_type: Optional[bool] = field(
        default=None,
        metadata={
            "name": "matchRtType",
            "type": "Attribute",
        },
    )
    allow_dummy_sections: Optional[bool] = field(
        default=None,
        metadata={
            "name": "allowDummySections",
            "type": "Attribute",
        },
    )
    enable_rt_full_search: Optional[bool] = field(
        default=None,
        metadata={
            "name": "enableRtFullSearch",
            "type": "Attribute",
        },
    )
    enable_replacements: Optional[bool] = field(
        default=None,
        metadata={
            "name": "enableReplacements",
            "type": "Attribute",
        },
    )
    with_journey_boundary_points: bool = field(
        default=False,
        metadata={
            "name": "withJourneyBoundaryPoints",
            "type": "Attribute",
        },
    )
    arr_l: Optional[int] = field(
        default=None,
        metadata={
            "name": "arrL",
            "type": "Attribute",
        },
    )
    arr_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "arrU",
            "type": "Attribute",
        },
    )
    dep_l: Optional[int] = field(
        default=None,
        metadata={
            "name": "depL",
            "type": "Attribute",
        },
    )
    dep_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "depU",
            "type": "Attribute",
        },
    )


@dataclass
class RoutingPreselectionType:
    gis_profile: Optional[GisProfile] = field(
        default=None,
        metadata={
            "name": "GisProfile",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    preselection_node: List[PreselectionNodeType] = field(
        default_factory=list,
        metadata={
            "name": "PreselectionNode",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class Stops:
    """
    The list of journey stops/stations.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    stop: List[StopType] = field(
        default_factory=list,
        metadata={
            "name": "Stop",
            "type": "Element",
            "min_occurs": 2,
        },
    )


@dataclass
class TrackData:
    """
    :ivar track_point: Tracked points.
    :ivar track_section: Key data relating to trip segments (journeys).
    :ivar algorithm:
    :ivar calc_match_quality: If set to true, result contains additional
        data about the match quality.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    track_point: List[TrackPoint] = field(
        default_factory=list,
        metadata={
            "name": "TrackPoint",
            "type": "Element",
        },
    )
    track_section: List[TrackSectionData] = field(
        default_factory=list,
        metadata={
            "name": "TrackSection",
            "type": "Element",
        },
    )
    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    calc_match_quality: Optional[bool] = field(
        default=None,
        metadata={
            "name": "calcMatchQuality",
            "type": "Attribute",
        },
    )


@dataclass
class FareItem:
    """
    :ivar ticket:
    :ivar param:
    :ivar external_content:
    :ivar name:
    :ivar desc:
    :ivar price:
    :ivar cur:
    :ivar shp_ctx:
    :ivar from_leg: Deprecated, use fromLegId. First leg this fare item
        is valid for.
    :ivar to_leg: Deprecated, use toLegId. Last leg this fare item is
        valid for.
    :ivar from_leg_id: First leg ID this fare item is valid for.
    :ivar to_leg_id: Last leg ID this fare item is valid for.
    """

    class Meta:
        name = "fareItem"
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ticket: List[Ticket] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    param: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    external_content: Optional[ExternalContentType] = field(
        default=None,
        metadata={
            "name": "externalContent",
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    price: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    cur: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shp_ctx: Optional[str] = field(
        default=None,
        metadata={
            "name": "shpCtx",
            "type": "Attribute",
        },
    )
    from_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "fromLeg",
            "type": "Attribute",
        },
    )
    to_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "toLeg",
            "type": "Attribute",
        },
    )
    from_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fromLegId",
            "type": "Attribute",
        },
    )
    to_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "toLegId",
            "type": "Attribute",
        },
    )


@dataclass
class CombinedProductType:
    """
    :ivar product: List of journey products for a journey section.
    """

    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )


@dataclass
class GeoFeatureList(CommonResponseType):
    """
    List of GeoFeature objects.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    geo_feature: List[GeoFeatureType] = field(
        default_factory=list,
        metadata={
            "name": "GeoFeature",
            "type": "Element",
        },
    )


@dataclass
class LocationPreselectionResponse(CommonResponseType):
    """
    Returns preselected nodes.

    :ivar reference_location: Reference location that serves as '1' in
        the requested 1:n or n:1
    :ivar preselection: Preselected nodes (transition locations) per
        requested routing strategy that serve as 'n' in the requested
        1:n or n:1
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    reference_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "referenceLocation",
            "type": "Element",
        },
    )
    preselection: List[PreselectionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class ManyToManyConnectionRequest:
    """
    :ivar origin:
    :ivar destination:
    :ivar via:
    :ivar avoid:
    :ivar front_preselection: List of preselected nodes per routing
        strategy that serve as entry points to public transport and are
        options to be used as front (first mile) of the resulting
        connections
    :ivar back_preselection: List of preselected nodes per routing
        strategy that serve as exit points from public transport and are
        options to be used as back (last mile) of the resulting
        connections
    :ivar gis_profile:
    :ivar filters:
    :ivar search_options:
    :ivar output_control:
    :ivar datetime: Date and time of departure or arrival.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    origin: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    destination: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    via: List[ViaType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    avoid: List[AvoidType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    front_preselection: List[RoutingPreselectionType] = field(
        default_factory=list,
        metadata={
            "name": "frontPreselection",
            "type": "Element",
        },
    )
    back_preselection: List[RoutingPreselectionType] = field(
        default_factory=list,
        metadata={
            "name": "backPreselection",
            "type": "Element",
        },
    )
    gis_profile: List[GisProfile] = field(
        default_factory=list,
        metadata={
            "name": "gisProfile",
            "type": "Element",
        },
    )
    filters: Optional[TripSearchFilterType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    search_options: Optional[SearchOptionsType] = field(
        default=None,
        metadata={
            "name": "searchOptions",
            "type": "Element",
            "required": True,
        },
    )
    output_control: Optional[OutputControlType] = field(
        default=None,
        metadata={
            "name": "outputControl",
            "type": "Element",
            "required": True,
        },
    )
    datetime: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Name:
    """
    Contains name of journey.

    :ivar product:
    :ivar name: Name to be displayed.
    :ivar add_name: Additional product name. This is customer specific.
    :ivar number: The train number.
    :ivar category: The train category.
    :ivar route_idx_from: Defines the first stop/station where this name
        is valid. See the Stops list for details of the stop/station.
    :ivar route_idx_to: Defines the last stop/station where this name is
        valid. See the Stops list for details of the stop/station.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    product: Optional[ProductType] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    add_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "addName",
            "type": "Attribute",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    category: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx_from: int = field(
        default=-1,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: int = field(
        default=-1,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )


@dataclass
class PartialTripSearchSettingsType:
    partial_search_replacement: Optional[PartialSearchReplacementType] = field(
        default=None,
        metadata={
            "name": "partialSearchReplacement",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    partial_search_segment: Optional[PartialSearchSegmentType] = field(
        default=None,
        metadata={
            "name": "partialSearchSegment",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )


@dataclass
class ProductCategoryType:
    """
    Product category info.

    :ivar product:
    :ivar name: Operator name for display.
    :ivar cls: Product category in decimal form.
    """

    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    cls: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class FareSetItem:
    """
    :ivar ticket_param:
    :ivar fare_item:
    :ivar param:
    :ivar name:
    :ivar desc:
    :ivar from_leg: Deprecated, use fromLegId. First leg this fare set
        is valid for.
    :ivar to_leg: Deprecated, use toLegId. Last leg this fare set is
        valid for.
    :ivar from_leg_id: First leg ID this fare set is valid for.
    :ivar to_leg_id: Last leg ID this fare set is valid for.
    """

    class Meta:
        name = "fareSetItem"
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ticket_param: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "ticketParam",
            "type": "Element",
        },
    )
    fare_item: List[FareItem] = field(
        default_factory=list,
        metadata={
            "name": "fareItem",
            "type": "Element",
        },
    )
    param: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    from_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "fromLeg",
            "type": "Attribute",
        },
    )
    to_leg: Optional[int] = field(
        default=None,
        metadata={
            "name": "toLeg",
            "type": "Attribute",
        },
    )
    from_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fromLegId",
            "type": "Attribute",
        },
    )
    to_leg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "toLegId",
            "type": "Attribute",
        },
    )


@dataclass
class DataInfo(CommonResponseType):
    """
    Contains information about master data.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    operator: List[OperatorType] = field(
        default_factory=list,
        metadata={
            "name": "Operator",
            "type": "Element",
        },
    )
    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    product_category: List[ProductCategoryType] = field(
        default_factory=list,
        metadata={
            "name": "ProductCategory",
            "type": "Element",
        },
    )
    region: List[RegionType] = field(
        default_factory=list,
        metadata={
            "name": "Region",
            "type": "Element",
        },
    )
    map_info: List[MapInfoType] = field(
        default_factory=list,
        metadata={
            "name": "MapInfo",
            "type": "Element",
        },
    )
    mobility_service_provider_info: List[MobilityServiceProviderInfoType] = (
        field(
            default_factory=list,
            metadata={
                "name": "MobilityServiceProviderInfo",
                "type": "Element",
            },
        )
    )
    begin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    end: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Names:
    """
    The list of journey names.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    name: List[Name] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class PartialTripSearchRequest:
    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    ctx: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "max_length": 8096,
        },
    )
    ps_settings: Optional[PartialTripSearchSettingsType] = field(
        default=None,
        metadata={
            "name": "psSettings",
            "type": "Element",
            "required": True,
        },
    )
    via: List[ViaType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    avoid: List[AvoidType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    gis_profile: List[GisProfile] = field(
        default_factory=list,
        metadata={
            "name": "gisProfile",
            "type": "Element",
        },
    )
    filters: Optional[TripSearchFilterType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    search_options: Optional[SearchOptionsType] = field(
        default=None,
        metadata={
            "name": "searchOptions",
            "type": "Element",
            "required": True,
        },
    )
    output_control: Optional[OutputControlType] = field(
        default=None,
        metadata={
            "name": "outputControl",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class TariffResult:
    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    fare_set_item: List[FareSetItem] = field(
        default_factory=list,
        metadata={
            "name": "fareSetItem",
            "type": "Element",
        },
    )
    clickout: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    external_content: Optional[ExternalContentType] = field(
        default=None,
        metadata={
            "name": "externalContent",
            "type": "Element",
        },
    )
    param: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class StopLocation:
    """
    The element StopLocation specifies a stop/station in a result of a location
    request.

    :ivar location_notes: Contains a list of notes to be displayed for
        this location, like attributes or footnotes.
    :ivar message:
    :ivar product_at_stop: Products running at this stop.
    :ivar tariff_result:
    :ivar links:
    :ivar alt_id:
    :ivar main_mast_alt_id:
    :ivar timezone_offset: Location time zone offset in minutes. Will
        only be filled in location-based services. If no date/time is
        specified in the request will return offset for current
        date/time.
    :ivar equivalent_stop_location: List of equivalent stop locations.
    :ivar entry_point_location: List of entry point locations.
    :ivar weather_information: Weather information for the given
        location - This is a list to support multiple information for
        one day or a 10-day-forecast or else. In the trivial case where
        the weather is requested for a specific point in time, this will
        only contain a single element.
    :ivar assigned_pois: Experimental! List of assigned POIs.
    :ivar id: This ID can either be used as originId or destId to
        perform a trip request or to call a departure or arrival board.
    :ivar ext_id: This ID defines an alternative ID for this stop
        location and can not be used to perform further requests.
    :ivar has_main_mast: True if this stop belongs to a main mast.
    :ivar main_mast_id: ID of the main mast this stop belongs to.
    :ivar main_mast_ext_id: External ID of the main mast this stop
        belongs to.
    :ivar main_mast_lon: The WGS84 longitude of the geographical
        position of the main mast this stop/station.
    :ivar main_mast_lat: The WGS84 latitude of the geographical position
        of the main mast this stop/station.
    :ivar main_mast_alt: The altitude of the geographical position of
        the main mast this stop/station.
    :ivar name: Contains the output name of this stop or station
    :ivar def_name: Contains the default name of this stop or station
    :ivar description: Additional description of location, e.g. address
    :ivar lon: The WGS84 longitude of the geographical position of the
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of the
        stop/station.
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar track: Track information, if available.
    :ivar track_hidden: True if track information is hidden by data.
    :ivar weight: This value specifies some kind of importance of this
        stop. The more traffic at this stop the higher the weight. The
        range is between 0 and 32767. This attribute is only available
        in the location.allstops response
    :ivar dist: This value specifies the distance to the given
        coordinate if called by a nearby search request.
    :ivar products: This value specifies the products available at this
        location.
    :ivar meta: True, if the stop is a meta stop.
    :ivar refinable: True, if the stop is not resolved fully and could
        be refined.
    :ivar match_value: A percentage value [0, 100] indicating how well
        the name of the given location matches the input location name.
        This attribute is only available in the location.name response
    :ivar entry: True, if the stop is an entry point.
    """

    location_notes: Optional[LocationNotes] = field(
        default=None,
        metadata={
            "name": "LocationNotes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    message: List["Message"] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    product_at_stop: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "productAtStop",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    tariff_result: Optional[TariffResult] = field(
        default=None,
        metadata={
            "name": "TariffResult",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    links: List[ResourceLinks] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    main_mast_alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "mainMastAltId",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    timezone_offset: Optional[int] = field(
        default=None,
        metadata={
            "name": "timezoneOffset",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    equivalent_stop_location: List["StopLocation"] = field(
        default_factory=list,
        metadata={
            "name": "equivalentStopLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    entry_point_location: List["StopLocation"] = field(
        default_factory=list,
        metadata={
            "name": "entryPointLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    weather_information: List[WeatherInformationType] = field(
        default_factory=list,
        metadata={
            "name": "weatherInformation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    assigned_pois: List[CoordLocation] = field(
        default_factory=list,
        metadata={
            "name": "assignedPois",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
            "required": True,
        },
    )
    has_main_mast: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasMainMast",
            "type": "Attribute",
        },
    )
    main_mast_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastId",
            "type": "Attribute",
        },
    )
    main_mast_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastExtId",
            "type": "Attribute",
        },
    )
    main_mast_lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLon",
            "type": "Attribute",
        },
    )
    main_mast_lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLat",
            "type": "Attribute",
        },
    )
    main_mast_alt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mainMastAlt",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    def_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "defName",
            "type": "Attribute",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track_hidden: bool = field(
        default=False,
        metadata={
            "name": "trackHidden",
            "type": "Attribute",
        },
    )
    weight: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    products: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    meta: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    refinable: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    match_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "matchValue",
            "type": "Attribute",
        },
    )
    entry: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AffectedStopType:
    """
    :ivar stop_location: List of stops affected by a message.
    """

    stop_location: List[StopLocation] = field(
        default_factory=list,
        metadata={
            "name": "StopLocation",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "min_occurs": 1,
        },
    )


@dataclass
class LocationDetails(CommonResponseType):
    """
    The location contains details for a stop/station or POI.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    stop_location: Optional[StopLocation] = field(
        default=None,
        metadata={
            "name": "StopLocation",
            "type": "Element",
        },
    )
    coord_location: Optional[CoordLocation] = field(
        default=None,
        metadata={
            "name": "CoordLocation",
            "type": "Element",
        },
    )


@dataclass
class LocationList(CommonResponseType):
    """The location list contains either named coordinates or stops/stations with
    name and id as a result of a location request.

    The data of every list entry can be used for further trip or
    departureBoard requests.

    :ivar stop_location:
    :ivar coord_location:
    :ivar scroll_ctx: In case of requested scrolling or too many
        results, use this context to get the next results.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    stop_location: List[StopLocation] = field(
        default_factory=list,
        metadata={
            "name": "StopLocation",
            "type": "Element",
        },
    )
    coord_location: List[CoordLocation] = field(
        default_factory=list,
        metadata={
            "name": "CoordLocation",
            "type": "Element",
        },
    )
    scroll_ctx: List[str] = field(
        default_factory=list,
        metadata={
            "name": "scrollCtx",
            "type": "Element",
        },
    )


@dataclass
class TrafficMessageType:
    icon: Optional[IconType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    location: Optional[StopLocation] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "PolylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
        },
    )
    type_value: Optional[TrafficMessageTypeType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    desc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Message:
    """
    Message.

    :ivar affected_product: Products affected by this message
    :ivar affected_journey: Products affected by this message
    :ivar edge: Edge this message is valid for.
    :ivar region: Region this message is valid for.
    :ivar event: Event period this message is valid for.
    :ivar affected_stops: Stops affected by this message
    :ivar valid_from_stop: Message is valid from this stop.
    :ivar valid_to_stop: Message is valid until this stop.
    :ivar tags: List of tags this message is tagged with.
    :ivar channel: List of publication channels along with its validity
        and optional URLs.
    :ivar message_category: List of message categories with its ID and
        optional localized name.
    :ivar message_text: List of messages texts with its tags and
        localized text fragments.
    :ivar validity_days: Days this message is valid for.
    :ivar note: List of notes to be displayed for this message.
    :ivar message: Child messages.
    :ivar id: ID of the message.
    :ivar external_id: External ID of the message if based on an
        external system.
    :ivar act: If message is active, value is true.
    :ivar head: Heading of message.
    :ivar lead: Preamble of message.
    :ivar text: Message text.
    :ivar text_internal: Internal message text.
    :ivar custom_text: Custom text.
    :ivar tckr: Deprecated. Message text for ticker display.
    :ivar company: Company whom created this message.
    :ivar category: Deprecated. See Message/MessageCategory. For sanity
        reason, id of first MessageCategory ist filled here.
    :ivar priority: Priority of the message.
    :ivar products: This value specifies the products affected by this
        message.
    :ivar icon:
    :ivar route_idx_from: First stop/station where this message is
        valid. See the Stops list in the JourneyDetail response for this
        leg to get more details about this stop/station.
    :ivar route_idx_to: Last stop/station where this message is valid.
        See the Stops list in the JourneyDetail response for this leg to
        get more details about this stop/station.
    :ivar s_time: Event period beginning time in format hh:mm[:ss]
    :ivar s_date: Event period beginning date in format YYYY-MM-DD.
    :ivar e_time: Event period ending time in format hh:mm[:ss]
    :ivar e_date: Event period ending date in format YYYY-MM-DD.
    :ivar alt_start: Descriptive text for start of event period.
    :ivar alt_end: Descriptive text for end of event period.
    :ivar mod_time: Message was last modified at time in format
        hh:mm[:ss]
    :ivar mod_date: Message was last modified at date in format YYYY-MM-
        DD.
    :ivar daily_starting_at: Message event period starting at time daily
        in format hh:mm[:ss]
    :ivar daily_duration: Message event period duration starting at
        dailyStartingAt for dailyDuration amount of time. Sample for 15
        hours: PT15H. Duration type definition
        https://www.w3.org/TR/xmlschema11-2/#duration.
    :ivar base_type: Contains the base type of the message.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    affected_product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "affectedProduct",
            "type": "Element",
        },
    )
    affected_journey: List["JourneyType"] = field(
        default_factory=list,
        metadata={
            "name": "affectedJourney",
            "type": "Element",
        },
    )
    edge: List[MessageEdgeType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    region: List[MessageRegionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    event: List[MessageEventType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    affected_stops: Optional[AffectedStopType] = field(
        default=None,
        metadata={
            "name": "affectedStops",
            "type": "Element",
        },
    )
    valid_from_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "validFromStop",
            "type": "Element",
        },
    )
    valid_to_stop: Optional[StopType] = field(
        default=None,
        metadata={
            "name": "validToStop",
            "type": "Element",
        },
    )
    tags: Optional[TagsType] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    channel: List[MessageChannelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    message_category: List[MessageCategoryType] = field(
        default_factory=list,
        metadata={
            "name": "messageCategory",
            "type": "Element",
        },
    )
    message_text: List[MessageTextType] = field(
        default_factory=list,
        metadata={
            "name": "messageText",
            "type": "Element",
        },
    )
    validity_days: Optional[ServiceDays] = field(
        default=None,
        metadata={
            "name": "validityDays",
            "type": "Element",
        },
    )
    note: List[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
        },
    )
    message: List["Message"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    external_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "externalId",
            "type": "Attribute",
        },
    )
    act: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    head: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lead: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    text_internal: Optional[str] = field(
        default=None,
        metadata={
            "name": "textInternal",
            "type": "Attribute",
        },
    )
    custom_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "customText",
            "type": "Attribute",
        },
    )
    tckr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    company: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    category: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    priority: int = field(
        default=100,
        metadata={
            "type": "Attribute",
        },
    )
    products: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    icon: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    route_idx_from: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxFrom",
            "type": "Attribute",
        },
    )
    route_idx_to: Optional[int] = field(
        default=None,
        metadata={
            "name": "routeIdxTo",
            "type": "Attribute",
        },
    )
    s_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "sTime",
            "type": "Attribute",
        },
    )
    s_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "sDate",
            "type": "Attribute",
        },
    )
    e_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "eTime",
            "type": "Attribute",
        },
    )
    e_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "eDate",
            "type": "Attribute",
        },
    )
    alt_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "altStart",
            "type": "Attribute",
        },
    )
    alt_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "altEnd",
            "type": "Attribute",
        },
    )
    mod_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "modTime",
            "type": "Attribute",
        },
    )
    mod_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "modDate",
            "type": "Attribute",
        },
    )
    daily_starting_at: Optional[str] = field(
        default=None,
        metadata={
            "name": "dailyStartingAt",
            "type": "Attribute",
        },
    )
    daily_duration: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "dailyDuration",
            "type": "Attribute",
        },
    )
    base_type: MessageBaseType = field(
        default=MessageBaseType.UNDEF,
        metadata={
            "name": "baseType",
            "type": "Attribute",
        },
    )


@dataclass
class HimMessages(CommonResponseType):
    """
    Contains notes to be displayed for this trip.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    message: List[Message] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
        },
    )


@dataclass
class Messages:
    """
    Contains notes to be displayed.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    message: List[Message] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class WalkingLinkType:
    """
    :ivar from_value: Location walking link starts at.
    :ivar to: Location walking link ends at.
    :ivar note: Notes related to that walking link.
    :ivar message: Messages related to that walking link.
    :ivar polyline_group: Polyline of that walking link.
    :ivar ext_id: External ID of walking link.
    """

    from_value: Optional[Location] = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    to: Optional[Location] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    note: List[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    message: List[Message] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "PolylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    ext_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "extId",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class GisRouteSegment:
    """
    :ivar notes:
    :ivar edge:
    :ivar traffic_message:
    :ivar messages:
    :ivar name: Segment name for display.
    :ivar r_type: Road type for this segment.
    :ivar r_num: Road number if available.
    :ivar man: Code for the manoeuvre to be executed.
    :ivar man_tx: Text description for the manoeuvre
    :ivar man_target_name: Name or description of the target of the
        current manoeuvre
    :ivar dir_tx: Direction text
    :ivar ori: Origin
    :ivar poly_s: Starting index into the polyline array.
    :ivar poly_e: End index into the polyline array
    :ivar dist: Distance for this segment in meter.
    :ivar dur_s: Duration for this segment in seconds.
    """

    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    edge: List[GisEdgeType] = field(
        default_factory=list,
        metadata={
            "name": "Edge",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    traffic_message: List[TrafficMessageType] = field(
        default_factory=list,
        metadata={
            "name": "TrafficMessage",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    r_type: Optional[GisRouteRoadType] = field(
        default=None,
        metadata={
            "name": "rType",
            "type": "Attribute",
        },
    )
    r_num: Optional[str] = field(
        default=None,
        metadata={
            "name": "rNum",
            "type": "Attribute",
        },
    )
    man: Optional[GisRouteManoeuvre] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    man_tx: Optional[str] = field(
        default=None,
        metadata={
            "name": "manTx",
            "type": "Attribute",
        },
    )
    man_target_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "manTargetName",
            "type": "Attribute",
        },
    )
    dir_tx: Optional[str] = field(
        default=None,
        metadata={
            "name": "dirTx",
            "type": "Attribute",
        },
    )
    ori: Optional[GisRouteOrientation] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    poly_s: Optional[int] = field(
        default=None,
        metadata={
            "name": "polyS",
            "type": "Attribute",
        },
    )
    poly_e: Optional[int] = field(
        default=None,
        metadata={
            "name": "polyE",
            "type": "Attribute",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dur_s: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durS",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyType:
    """The element Journey contains all information about a journey like name,
    direction, lon, lat, train number and train category.

    It also contains a reference to journey.

    :ivar journey_origin: Represents the first stop of this journey.
    :ivar journey_destination: Represents the last stop of this journey.
    :ivar stops:
    :ivar journey_detail_ref:
    :ivar product: Product context, provides access to internal data
    :ivar notes:
    :ivar messages:
    :ivar occupancy:
    :ivar referenced_journey: Referenced journeys
    :ivar journey_path: Journey path to represent journey position
        information for animated live map view.
    :ivar name: Specifies the name of the journey (e.g. "Bus 100") as
        used for display.
    :ivar add_name: Additional product name. This is customer specific.
    :ivar direction: Direction information. This is the last stop of the
        journey. Get the full journey of the train or bus with the
        JourneyDetails service.
    :ivar lon: The current longitude position of the journey.
    :ivar lat: The current latitude position of the journey.
    :ivar alt: The current altitude position of the journey.
    :ivar train_number: Train number as used for display.
    :ivar train_category: Train category as used for display.
    """

    journey_origin: Optional[OriginDestType] = field(
        default=None,
        metadata={
            "name": "JourneyOrigin",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey_destination: Optional[OriginDestType] = field(
        default=None,
        metadata={
            "name": "JourneyDestination",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    stops: Optional[Stops] = field(
        default=None,
        metadata={
            "name": "Stops",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey_detail_ref: Optional[JourneyDetailRef] = field(
        default=None,
        metadata={
            "name": "JourneyDetailRef",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    product: Optional[ProductType] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    referenced_journey: List["ReferencedJourneyType"] = field(
        default_factory=list,
        metadata={
            "name": "referencedJourney",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey_path: Optional[JourneyPathType] = field(
        default=None,
        metadata={
            "name": "JourneyPath",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    add_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "addName",
            "type": "Attribute",
        },
    )
    direction: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    train_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainNumber",
            "type": "Attribute",
        },
    )
    train_category: Optional[str] = field(
        default=None,
        metadata={
            "name": "trainCategory",
            "type": "Attribute",
        },
    )


@dataclass
class WalkingLinks(CommonResponseType):
    """
    Contains information about walking links at stations.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    walking_link: List[WalkingLinkType] = field(
        default_factory=list,
        metadata={
            "name": "WalkingLink",
            "type": "Element",
        },
    )


@dataclass
class FreqType:
    """
    Alternatives for this leg by plan.

    :ivar journey: List of alternative legs.
    :ivar wait_minimum: Shortest wait time (in minutes).
    :ivar wait_maximum: Longest wait time (in minutes).
    :ivar alternative_count: Count of alternative legs.
    """

    journey: List[JourneyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    wait_minimum: Optional[int] = field(
        default=None,
        metadata={
            "name": "waitMinimum",
            "type": "Attribute",
        },
    )
    wait_maximum: Optional[int] = field(
        default=None,
        metadata={
            "name": "waitMaximum",
            "type": "Attribute",
        },
    )
    alternative_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "alternativeCount",
            "type": "Attribute",
        },
    )


@dataclass
class GisRouteType:
    """
    :ivar seg:
    :ivar notes:
    :ivar polyline:
    :ivar polyline_group:
    :ivar alt_polyline:
    :ivar alt_polyline_group:
    :ivar dist: Distance for this GIS route in meter.
    :ivar dur_s: Duration for this GIS route in seconds.
    :ivar dur_r: Duration for this GIS route in seconds based on the
        realtime situation.
    :ivar dur_st: Estimated search time for a parking place in seconds.
    :ivar dur_w2_c: Estimated walking time from the starting address to
        the parking place in seconds.
    :ivar dur_w2_d: Estimated walking time from the destination parking
        place to the destination address in seconds.
    :ivar dir_txt: Direction text
    :ivar dir_geo: Geographical direction of the route. The direction
        range is from 0 to 31 with 0 starting from the x-axis in
        mathematical positive direction.
    :ivar edge_hash_s: Hash-Value over the edge list that represented
        the segments of the polyline when it was originally searched.
    :ivar edge_hash_r: Hash-Value over the edge list that represents the
        segments of the polyline for the current request.
    :ivar tot_uphill: Total uphill in meter
    :ivar tot_downhill: Total downhill in meter
    """

    seg: List[GisRouteSegment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline: Optional[Polyline] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "polylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alt_polyline: List[Polyline] = field(
        default_factory=list,
        metadata={
            "name": "altPolyline",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alt_polyline_group: List[PolylineGroup] = field(
        default_factory=list,
        metadata={
            "name": "altPolylineGroup",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dur_s: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durS",
            "type": "Attribute",
        },
    )
    dur_r: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durR",
            "type": "Attribute",
        },
    )
    dur_st: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durST",
            "type": "Attribute",
        },
    )
    dur_w2_c: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durW2C",
            "type": "Attribute",
        },
    )
    dur_w2_d: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durW2D",
            "type": "Attribute",
        },
    )
    dir_txt: Optional[str] = field(
        default=None,
        metadata={
            "name": "dirTxt",
            "type": "Attribute",
        },
    )
    dir_geo: Optional[int] = field(
        default=None,
        metadata={
            "name": "dirGeo",
            "type": "Attribute",
        },
    )
    edge_hash_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "edgeHashS",
            "type": "Attribute",
        },
    )
    edge_hash_r: Optional[str] = field(
        default=None,
        metadata={
            "name": "edgeHashR",
            "type": "Attribute",
        },
    )
    tot_uphill: Optional[float] = field(
        default=None,
        metadata={
            "name": "totUphill",
            "type": "Attribute",
        },
    )
    tot_downhill: Optional[float] = field(
        default=None,
        metadata={
            "name": "totDownhill",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyList(CommonResponseType):
    """
    A list of journeys.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey: List[JourneyType] = field(
        default_factory=list,
        metadata={
            "name": "Journey",
            "type": "Element",
        },
    )


@dataclass
class LineType:
    product: Optional[ProductType] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    journey: List[JourneyType] = field(
        default_factory=list,
        metadata={
            "name": "Journey",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
            "required": True,
        },
    )
    direction: List[Direction] = field(
        default_factory=list,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    line_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineId",
            "type": "Attribute",
            "required": True,
        },
    )
    line_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineName",
            "type": "Attribute",
        },
    )
    line_name_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "lineNameShort",
            "type": "Attribute",
        },
    )


@dataclass
class ReferencedJourneyType:
    journey: Optional[JourneyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    type_value: Optional[ReferencedJourneyTypeType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    orig_from_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "origFromIdx",
            "type": "Attribute",
        },
    )
    orig_to_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "origToIdx",
            "type": "Attribute",
        },
    )
    ref_from_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "refFromIdx",
            "type": "Attribute",
        },
    )
    ref_to_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "refToIdx",
            "type": "Attribute",
        },
    )


@dataclass
class Arrival:
    """The element Arrival contains all information about a arrival like time,
    date, stop/station name, track, realtime time, date and track, origin, name and
    type of the journey.

    It also contains a reference to journey details.

    :ivar journey_detail_ref:
    :ivar journey_status:
    :ivar product_at_stop:
    :ivar product:
    :ivar notes:
    :ivar messages:
    :ivar directions:
    :ivar alt_id:
    :ivar main_mast_alt_id:
    :ivar stops:
    :ivar occupancy:
    :ivar referenced_journey: Referenced journeys
    :ivar platform:
    :ivar rt_platform:
    :ivar name: Specifies the name of the arriving journey (e.g. "Bus
        100") as used for display.
    :ivar type_value: The attribute type specifies the type of arrivals
        location. Valid values are ST (stop/station), ADR (address), POI
        (point of interest), CRD (coordinate), MCP (mode change point)
        or HL (hailing point).
    :ivar stop: Contains the name of the stop/station.
    :ivar stopid: Contains the ID of the stop/station.
    :ivar stop_ext_id: External ID of this stop/station
    :ivar lon: The WGS84 longitude of the geographical position of this
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of this
        stop/station.
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar has_main_mast: True if this stop belongs to a main mast.
    :ivar main_mast_id: ID of the main mast this stop belongs to.
    :ivar main_mast_ext_id: External ID of the main mast this stop
        belongs to.
    :ivar main_mast_lon: The WGS84 longitude of the geographical
        position of the main mast this stop/station.
    :ivar main_mast_lat: The WGS84 latitude of the geographical position
        of the main mast this stop/station.
    :ivar main_mast_alt: The altitude of the geographical position of
        the main mast this stop/station.
    :ivar prognosis_type: Prognosis type of arrival date and time.
    :ivar time: Time in format hh:mm[:ss]
    :ivar date: Date in format YYYY-MM-DD.
    :ivar scheduled_time_changed: Scheduled time changed.
    :ivar tz: Time zone information in the format +/- minutes
    :ivar track: Arrival track information, if available.
    :ivar track_hidden: True if track information is hidden by data.
    :ivar rt_time: Realtime time in format hh:mm[:ss] if available.
    :ivar rt_date: Realtime date in format YYYY-MM-DD, if available.
    :ivar rt_tz: Realtime timezone in the format +/- minutes, if
        available.
    :ivar rt_track: Realtime track information, if available.
    :ivar rt_track_hidden: True if track information is hidden by
        realtime data.
    :ivar cancelled: Will be true if this journey is cancelled
    :ivar part_cancelled: Will be true if this journey is partially
        cancelled.
    :ivar reachable: Will be true if this journey is reachable. A
        journey is considered reachable if either the follow-up journey
        is reachable based on the scheduled time (default without
        realtime) or the followup journey is not reachable regarding
        realtime situation but reported as reachable explicitly.
    :ivar redirected: Will be true if this journey is redirected. A
        journey is considered as redirected if structural changes (e.g.
        additional/removed stop, change of scheduled times, ...) have
        been made.
    :ivar uncertain_delay: The journey stopped or is waiting somewhere
        along its path and some journey stops contain an uncertain
        delay.
    :ivar origin: Origin of the journey. This is the first stop of the
        journey. Get the full journey of the train or bus with the
        JourneyDetails service.
    :ivar direction_flag: Direction flag of the journey.
    :ivar is_border_stop: Will be true if this stop is a border stop
    :ivar is_turning_point: Will be true if this stop is a turning point
    :ivar entry: True, if the stop is an entry point.
    :ivar rt_cncl_data_source_type: Realtime data source that the stop
        cancellation originates from
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail_ref: Optional[JourneyDetailRef] = field(
        default=None,
        metadata={
            "name": "JourneyDetailRef",
            "type": "Element",
            "required": True,
        },
    )
    journey_status: Optional[JourneyStatusType] = field(
        default=None,
        metadata={
            "name": "JourneyStatus",
            "type": "Element",
        },
    )
    product_at_stop: Optional[ProductType] = field(
        default=None,
        metadata={
            "name": "ProductAtStop",
            "type": "Element",
        },
    )
    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
        },
    )
    directions: Optional[Directions] = field(
        default=None,
        metadata={
            "name": "Directions",
            "type": "Element",
        },
    )
    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
        },
    )
    main_mast_alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "mainMastAltId",
            "type": "Element",
        },
    )
    stops: Optional[Stops] = field(
        default=None,
        metadata={
            "name": "Stops",
            "type": "Element",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
        },
    )
    referenced_journey: List[ReferencedJourneyType] = field(
        default_factory=list,
        metadata={
            "name": "referencedJourney",
            "type": "Element",
        },
    )
    platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    rt_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "rtPlatform",
            "type": "Element",
        },
    )
    name: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type_value: Optional[ArrivalType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    stop: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    stopid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    stop_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "stopExtId",
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    has_main_mast: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasMainMast",
            "type": "Attribute",
        },
    )
    main_mast_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastId",
            "type": "Attribute",
        },
    )
    main_mast_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastExtId",
            "type": "Attribute",
        },
    )
    main_mast_lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLon",
            "type": "Attribute",
        },
    )
    main_mast_lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLat",
            "type": "Attribute",
        },
    )
    main_mast_alt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mainMastAlt",
            "type": "Attribute",
        },
    )
    prognosis_type: Optional[PrognosisType] = field(
        default=None,
        metadata={
            "name": "prognosisType",
            "type": "Attribute",
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    scheduled_time_changed: bool = field(
        default=False,
        metadata={
            "name": "scheduledTimeChanged",
            "type": "Attribute",
        },
    )
    tz: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track_hidden: bool = field(
        default=False,
        metadata={
            "name": "trackHidden",
            "type": "Attribute",
        },
    )
    rt_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTime",
            "type": "Attribute",
        },
    )
    rt_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDate",
            "type": "Attribute",
        },
    )
    rt_tz: int = field(
        default=0,
        metadata={
            "name": "rtTz",
            "type": "Attribute",
        },
    )
    rt_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTrack",
            "type": "Attribute",
        },
    )
    rt_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "rtTrackHidden",
            "type": "Attribute",
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    part_cancelled: bool = field(
        default=False,
        metadata={
            "name": "partCancelled",
            "type": "Attribute",
        },
    )
    reachable: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    redirected: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "uncertainDelay",
            "type": "Attribute",
        },
    )
    origin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    direction_flag: Optional[str] = field(
        default=None,
        metadata={
            "name": "directionFlag",
            "type": "Attribute",
        },
    )
    is_border_stop: bool = field(
        default=False,
        metadata={
            "name": "isBorderStop",
            "type": "Attribute",
        },
    )
    is_turning_point: bool = field(
        default=False,
        metadata={
            "name": "isTurningPoint",
            "type": "Attribute",
        },
    )
    entry: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rt_cncl_data_source_type: Optional[RealtimeDataSourceType] = field(
        default=None,
        metadata={
            "name": "rtCnclDataSourceType",
            "type": "Attribute",
        },
    )


@dataclass
class Departure:
    """The element Departure contains all information about a departure like time,
    date, stop/station name, track, realtime time, date and track, direction, name
    and type of the journey.

    It also contains a reference to journey details.

    :ivar journey_detail_ref:
    :ivar journey_status:
    :ivar product_at_stop:
    :ivar product:
    :ivar notes:
    :ivar messages:
    :ivar directions:
    :ivar alt_id:
    :ivar main_mast_alt_id:
    :ivar stops:
    :ivar occupancy:
    :ivar parallel_journey_ref:
    :ivar referenced_journey: Referenced journeys
    :ivar platform:
    :ivar rt_platform:
    :ivar name: Specifies the name of the departing journey (e.g. "Bus
        100") as used for display.
    :ivar type_value: The attribute type specifies the type of departs
        location. Valid values are ST (stop/station), ADR (address), POI
        (point of interest), CRD (coordinate), MCP (mode change point)
        or HL (hailing point).
    :ivar stop: Contains the name of the stop/station.
    :ivar stopid: Contains the ID of the stop/station.
    :ivar stop_ext_id: External ID of this stop/station
    :ivar lon: The WGS84 longitude of the geographical position of this
        stop/station.
    :ivar lat: The WGS84 latitude of the geographical position of this
        stop/station.
    :ivar alt: The altitude of the geographical position of this
        stop/station.
    :ivar has_main_mast: True if this stop belongs to a main mast.
    :ivar main_mast_id: ID of the main mast this stop belongs to.
    :ivar main_mast_ext_id: External ID of the main mast this stop
        belongs to.
    :ivar main_mast_lon: The WGS84 longitude of the geographical
        position of the main mast this stop/station.
    :ivar main_mast_lat: The WGS84 latitude of the geographical position
        of the main mast this stop/station.
    :ivar main_mast_alt: The altitude of the geographical position of
        the main mast this stop/station.
    :ivar prognosis_type: Prognosis type of departure date and time.
    :ivar time: Time in format hh:mm[:ss]
    :ivar scheduled_time_changed: Scheduled time changed.
    :ivar date: Date in format YYYY-MM-DD.
    :ivar tz: Time zone information in the format +/- minutes
    :ivar track: Track information, if available.
    :ivar track_hidden: True if track information is hidden by data.
    :ivar rt_time: Realtime time in format hh:mm[:ss] if available.
    :ivar rt_date: Realtime date in format YYYY-MM-DD, if available.
    :ivar rt_tz: Realtime time zone information in the format +/-
        minutes, if available.
    :ivar rt_track: Realtime track information, if available.
    :ivar rt_track_hidden: True if track information is hidden by
        realtime data.
    :ivar cancelled: Will be true if this journey is cancelled
    :ivar part_cancelled: Will be true if this journey is partially
        cancelled.
    :ivar reachable: Will be true if this journey is reachable. A
        journey is considered reachable if either the follow-up journey
        is reachable based on the scheduled time (default without
        realtime) or the followup journey is not reachable regarding
        realtime situation but reported as reachable explicitly.
    :ivar redirected: Will be true if this journey is redirected. A
        journey is considered as redirected if structural changes (e.g.
        additional/removed stop, change of scheduled times, ...) have
        been made.
    :ivar direction: Direction information. This is the last stop of the
        journey. Get the full journey of the train or bus with the
        JourneyDetails service.
    :ivar direction_flag: Direction flag of the journey.
    :ivar direction_ext_id: External ID of direction stop/station
    :ivar time_at_arrival: Time in format hh:mm[:ss] the services
        arrives at the destination.
    :ivar date_at_arrival: Date in format YYYY-MM-DD the services
        arrives at the destination.
    :ivar rt_time_at_arrival: Realtime time in format hh:mm[:ss] the
        services arrives at the destination.
    :ivar rt_date_at_arrival: Realtime date in format YYYY-MM-DD the
        services arrives at the destination.
    :ivar is_fastest: Services is 'fastest service to' location.
    :ivar is_border_stop: Will be true if this stop is a border stop
    :ivar is_turning_point: Will be true if this stop is a turning point
    :ivar entry: True, if the stop is an entry point.
    :ivar rt_cncl_data_source_type: Realtime data source that the stop
        cancellation originates from
    :ivar uncertain_delay: The journey stopped or is waiting somewhere
        along its path and some journey stops contain an uncertain
        delay.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail_ref: Optional[JourneyDetailRef] = field(
        default=None,
        metadata={
            "name": "JourneyDetailRef",
            "type": "Element",
            "required": True,
        },
    )
    journey_status: Optional[JourneyStatusType] = field(
        default=None,
        metadata={
            "name": "JourneyStatus",
            "type": "Element",
        },
    )
    product_at_stop: Optional[ProductType] = field(
        default=None,
        metadata={
            "name": "ProductAtStop",
            "type": "Element",
        },
    )
    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
        },
    )
    directions: Optional[Directions] = field(
        default=None,
        metadata={
            "name": "Directions",
            "type": "Element",
        },
    )
    alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "altId",
            "type": "Element",
        },
    )
    main_mast_alt_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "mainMastAltId",
            "type": "Element",
        },
    )
    stops: Optional[Stops] = field(
        default=None,
        metadata={
            "name": "Stops",
            "type": "Element",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
        },
    )
    parallel_journey_ref: List[ParallelJourneyRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParallelJourneyRef",
            "type": "Element",
        },
    )
    referenced_journey: List[ReferencedJourneyType] = field(
        default_factory=list,
        metadata={
            "name": "referencedJourney",
            "type": "Element",
        },
    )
    platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    rt_platform: Optional[PlatformType] = field(
        default=None,
        metadata={
            "name": "rtPlatform",
            "type": "Element",
        },
    )
    name: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type_value: Optional[DepartureType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    stop: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    stopid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    stop_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "stopExtId",
            "type": "Attribute",
        },
    )
    lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    has_main_mast: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasMainMast",
            "type": "Attribute",
        },
    )
    main_mast_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastId",
            "type": "Attribute",
        },
    )
    main_mast_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainMastExtId",
            "type": "Attribute",
        },
    )
    main_mast_lon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLon",
            "type": "Attribute",
        },
    )
    main_mast_lat: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "mainMastLat",
            "type": "Attribute",
        },
    )
    main_mast_alt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mainMastAlt",
            "type": "Attribute",
        },
    )
    prognosis_type: Optional[PrognosisType] = field(
        default=None,
        metadata={
            "name": "prognosisType",
            "type": "Attribute",
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    scheduled_time_changed: bool = field(
        default=False,
        metadata={
            "name": "scheduledTimeChanged",
            "type": "Attribute",
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tz: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track_hidden: bool = field(
        default=False,
        metadata={
            "name": "trackHidden",
            "type": "Attribute",
        },
    )
    rt_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTime",
            "type": "Attribute",
        },
    )
    rt_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDate",
            "type": "Attribute",
        },
    )
    rt_tz: int = field(
        default=0,
        metadata={
            "name": "rtTz",
            "type": "Attribute",
        },
    )
    rt_track: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTrack",
            "type": "Attribute",
        },
    )
    rt_track_hidden: bool = field(
        default=False,
        metadata={
            "name": "rtTrackHidden",
            "type": "Attribute",
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    part_cancelled: bool = field(
        default=False,
        metadata={
            "name": "partCancelled",
            "type": "Attribute",
        },
    )
    reachable: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    redirected: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    direction: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    direction_flag: Optional[str] = field(
        default=None,
        metadata={
            "name": "directionFlag",
            "type": "Attribute",
        },
    )
    direction_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "directionExtId",
            "type": "Attribute",
        },
    )
    time_at_arrival: Optional[str] = field(
        default=None,
        metadata={
            "name": "timeAtArrival",
            "type": "Attribute",
        },
    )
    date_at_arrival: Optional[str] = field(
        default=None,
        metadata={
            "name": "dateAtArrival",
            "type": "Attribute",
        },
    )
    rt_time_at_arrival: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtTimeAtArrival",
            "type": "Attribute",
        },
    )
    rt_date_at_arrival: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtDateAtArrival",
            "type": "Attribute",
        },
    )
    is_fastest: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isFastest",
            "type": "Attribute",
        },
    )
    is_border_stop: bool = field(
        default=False,
        metadata={
            "name": "isBorderStop",
            "type": "Attribute",
        },
    )
    is_turning_point: bool = field(
        default=False,
        metadata={
            "name": "isTurningPoint",
            "type": "Attribute",
        },
    )
    entry: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rt_cncl_data_source_type: Optional[RealtimeDataSourceType] = field(
        default=None,
        metadata={
            "name": "rtCnclDataSourceType",
            "type": "Attribute",
        },
    )
    uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "uncertainDelay",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyDetail(CommonResponseType):
    """The journey details contain a list of stops/stations and notes.

    They also contain the journeys names and types.

    :ivar stops:
    :ivar names: Deprecated. Use Product* instead.
    :ivar product:
    :ivar directions:
    :ivar notes: Contains notes to be displayed for this trip like
        attributes or footnotes.
    :ivar messages:
    :ivar journey_status:
    :ivar polyline:
    :ivar polyline_group:
    :ivar service_days:
    :ivar referenced_journey: Referenced journeys
    :ivar last_pos: Last position of running journey if any.
    :ivar last_pos_reported: Date and time of last position reported if
        any.
    :ivar last_pass_route_idx: Last passed stop referencing the route
        index of that stop, even if out of this part of the journey.
    :ivar last_pass_stop_ref: Last passed stop referencing the entry
        index in the stop list, even if out of this part of the journey.
    :ivar rt_last_pass_route_idx: Last passed stop referencing the route
        index of that stop, even if out of this part of the journey,
        real time situation.
    :ivar rt_last_pass_stop_ref: Last passed stop referencing the entry
        index in the stop list, even if out of this part of the journey.
    :ivar parallel_journey_ref:
    :ivar cancelled: Will be true if this journey is cancelled.
    :ivar part_cancelled: Will be true if this journey is partially
        cancelled.
    :ivar reachable: Will be true if this journey is reachable. A
        journey is considered reachable if either the follow-up journey
        is reachable based on the scheduled time (default without
        realtime) or the followup journey is not reachable regarding
        realtime situation but reported as reachable explicitly.
    :ivar redirected: Will be true if this journey is redirected. A
        journey is considered as redirected if structural changes (e.g.
        additional/removed stop, change of scheduled times, ...) have
        been made.
    :ivar uncertain_delay: The journey stopped or is waiting somewhere
        along its path and some journey stops contain an uncertain
        delay.
    :ivar day_of_operation: Date on which the journey departs at the
        first passlist stop of the full journey. Is in no way guaranteed
        to be related to the times of the passlist stops in any way.
        Date in format YYYY-MM-DD.
    :ivar ref: Contains an internal journey id which must use for a
        subsequent journey detail request.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    stops: Optional[Stops] = field(
        default=None,
        metadata={
            "name": "Stops",
            "type": "Element",
        },
    )
    names: Optional[Names] = field(
        default=None,
        metadata={
            "name": "Names",
            "type": "Element",
        },
    )
    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    directions: Optional[Directions] = field(
        default=None,
        metadata={
            "name": "Directions",
            "type": "Element",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
        },
    )
    journey_status: Optional[JourneyStatusType] = field(
        default=None,
        metadata={
            "name": "JourneyStatus",
            "type": "Element",
        },
    )
    polyline: Optional[Polyline] = field(
        default=None,
        metadata={
            "name": "Polyline",
            "type": "Element",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "PolylineGroup",
            "type": "Element",
        },
    )
    service_days: List[ServiceDays] = field(
        default_factory=list,
        metadata={
            "name": "ServiceDays",
            "type": "Element",
        },
    )
    referenced_journey: List[ReferencedJourneyType] = field(
        default_factory=list,
        metadata={
            "name": "referencedJourney",
            "type": "Element",
        },
    )
    last_pos: Optional[Coordinate] = field(
        default=None,
        metadata={
            "name": "lastPos",
            "type": "Element",
        },
    )
    last_pos_reported: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastPosReported",
            "type": "Element",
        },
    )
    last_pass_route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "lastPassRouteIdx",
            "type": "Element",
        },
    )
    last_pass_stop_ref: Optional[int] = field(
        default=None,
        metadata={
            "name": "lastPassStopRef",
            "type": "Element",
        },
    )
    rt_last_pass_route_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "rtLastPassRouteIdx",
            "type": "Element",
        },
    )
    rt_last_pass_stop_ref: Optional[int] = field(
        default=None,
        metadata={
            "name": "rtLastPassStopRef",
            "type": "Element",
        },
    )
    parallel_journey_ref: List[ParallelJourneyRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParallelJourneyRef",
            "type": "Element",
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    part_cancelled: bool = field(
        default=False,
        metadata={
            "name": "partCancelled",
            "type": "Attribute",
        },
    )
    reachable: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    redirected: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "uncertainDelay",
            "type": "Attribute",
        },
    )
    day_of_operation: Optional[str] = field(
        default=None,
        metadata={
            "name": "dayOfOperation",
            "type": "Attribute",
            "required": True,
        },
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "max_length": 512,
        },
    )


@dataclass
class LineList(CommonResponseType):
    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    line: List[LineType] = field(
        default_factory=list,
        metadata={
            "name": "Line",
            "type": "Element",
        },
    )


@dataclass
class ArrivalBoard(CommonResponseType):
    """
    The arrival board lists arrivals at a specific stop/station or group of
    stop/stations.

    :ivar arrival: The element Arrival contains all information about a
        arrival like time, date, stop/station name, track, realtime
        time, date and track, origin, name and type of the journey. It
        also contains a reference to journey details.
    :ivar message:
    :ivar stopid: Contains the ID of the stop/station.
    :ivar stop_ext_id: External ID of this stop/station
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    arrival: List[Arrival] = field(
        default_factory=list,
        metadata={
            "name": "Arrival",
            "type": "Element",
        },
    )
    message: List[Message] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
        },
    )
    stopid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    stop_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "stopExtId",
            "type": "Attribute",
        },
    )


@dataclass
class DepartureBoard(CommonResponseType):
    """
    The departure board lists departures at a specific stop/station or group of
    stop/stations.

    :ivar departure: The element Departure contains all information
        about a departure like time, date, stop/station name, track,
        realtime time, date and track, direction, name and type of the
        journey. It also contains a reference to journey details.
    :ivar message:
    :ivar stopid: Contains the ID of the stop/station.
    :ivar stop_ext_id: External ID of this stop/station
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    departure: List[Departure] = field(
        default_factory=list,
        metadata={
            "name": "Departure",
            "type": "Element",
        },
    )
    message: List[Message] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
        },
    )
    stopid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    stop_ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "stopExtId",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyDetailGroup:
    """
    A group of detailed journeys.

    :ivar journey_detail:
    :ivar name: Name of this group.
    :ivar name_s: Short name of this group.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail: List[JourneyDetail] = field(
        default_factory=list,
        metadata={
            "name": "JourneyDetail",
            "type": "Element",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name_s: Optional[str] = field(
        default=None,
        metadata={
            "name": "nameS",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyDetailList(CommonResponseType):
    """
    A list of detailed journeys.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail: List[JourneyDetail] = field(
        default_factory=list,
        metadata={
            "name": "JourneyDetail",
            "type": "Element",
        },
    )


@dataclass
class Leg:
    """A leg is one part of a trip.

    It can be either a walk, a bike or car ride or (in most cases) a
    journey by bus, train or some other means of transport.

    :ivar origin:
    :ivar destination:
    :ivar journey_origin: Represents the first stop of the unterlying
        journey in case of an public transport leg.
    :ivar journey_destination: Represents the last stop of the
        unterlying journey in case of an public transport leg.
    :ivar notes:
    :ivar journey_detail_ref:
    :ivar freq:
    :ivar gis_ref:
    :ivar gis_route:
    :ivar messages:
    :ivar traffic_message:
    :ivar journey_status:
    :ivar product:
    :ivar combined_product: List of products for all combined journeys
        attributed to this journey.
    :ivar polyline:
    :ivar polyline_group:
    :ivar stops:
    :ivar service_days:
    :ivar journey_detail:
    :ivar parallel_journey:
    :ivar occupancy:
    :ivar referenced_journey: Referenced journeys
    :ivar id: Unique ID for the leg, relative to the trip. Not stable
        and only valid within the given response.
    :ivar idx: Specifies the index of the leg starting from 0 and
        incrementing by 1. It corresponds to travel-order ascending;
        unique within composite Trip.
    :ivar name: The attribute name specifies the name of the leg. The
        name might be composed from product number, line and/or category
        (e.g. "Bus 100"). This is customer specific. In case of a non
        public transport leg like bike, car, taxi or walk, this field is
        filled with a localized value for the specific type. Same for
        check-in or check-out. Samples: - Walk -&gt; Chemin piéton
        (French), Gå (Danish)... - Transfer -&gt; Transfert (French), Gå
        (Udveksling)... Those localizations can be configured in the
        underlying HAFAS system. In case of a sharing provider, this
        field might be filled with provider name if data covers that.
    :ivar add_name: Additional product name. This is customer specific.
    :ivar number: The train number.
    :ivar category: The train category name. The category assignments
        are stored in the "zugart" file of the raw Hafas plan data.
    :ivar type_value: The attribute type specifies the type of the leg.
        The value can be the JNY for public transport or WALK, TRSF
        (transfer), BIKE, KISS (car), PARK (Park and Ride) or TAXI, CHKI
        (check-in), CHKO (check-out), TETA (Tele taxi) or DUMMY (in case
        of not reconstructable leg).
    :ivar cancelled: Will be true if this journey is cancelled.
    :ivar part_cancelled: Will be true if this journey is partially
        cancelled.
    :ivar reachable: Will be true if this journey is reachable. A
        journey is considered reachable if either the follow-up journey
        is reachable based on the scheduled time (default without
        realtime) or the followup journey is not reachable regarding
        realtime situation but reported as reachable explicitly.
    :ivar redirected: Will be true if this journey is redirected. A
        journey is considered as redirected if structural changes (e.g.
        additional/removed stop, change of scheduled times, ...) have
        been made.
    :ivar direction: Direction information. This will be the name of the
        last station of the train's journey. Call the JourneyDetail
        service to get detailed information about the train journey.
    :ivar direction_flag: Direction flag of the journey.
    :ivar duration: The duration.
    :ivar dist: Distance for this leg in meter.
    :ivar hide: Will be true if this journey is hidden.
    :ivar ps_ctx_arrive_earlier: Provides a context that may be used in
        service PartialSearch to increase the time for interchange
        between the previous journey arrival stop and the following
        journey departure stop by searching a trip that will lead to an
        earlier arrival time for the previous journey while keeping the
        departure time for the following journey(s) constant.
    :ivar ps_ctx_depart_later: Provides a context that may be used in
        service PartialSearch to increase the time for interchange
        between the previous journey arrival stop and the following
        journey departure stop by searching a trip that will lead to a
        later departure time for the following journey while keeping the
        arrival time for the previous journey(s) constant.
    :ivar rec_state: Contains the outcome information for the section,
        if it resulted from a reconstruction.
    :ivar change_assured: Indicates whether a journey is reachable
        because the change is explicitly assured (true), not reachable
        because the change is explicitly not assured (false) or no
        relevant realtime information is available (no value set).
    :ivar uncertain_delay: The journey stopped or is waiting somewhere
        along its path and some journey stops contain an uncertain
        delay.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    origin: Optional[Origin] = field(
        default=None,
        metadata={
            "name": "Origin",
            "type": "Element",
            "required": True,
        },
    )
    destination: Optional[Destination] = field(
        default=None,
        metadata={
            "name": "Destination",
            "type": "Element",
            "required": True,
        },
    )
    journey_origin: Optional[OriginDestType] = field(
        default=None,
        metadata={
            "name": "JourneyOrigin",
            "type": "Element",
        },
    )
    journey_destination: Optional[OriginDestType] = field(
        default=None,
        metadata={
            "name": "JourneyDestination",
            "type": "Element",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        },
    )
    journey_detail_ref: Optional[JourneyDetailRef] = field(
        default=None,
        metadata={
            "name": "JourneyDetailRef",
            "type": "Element",
        },
    )
    freq: Optional[FreqType] = field(
        default=None,
        metadata={
            "name": "Freq",
            "type": "Element",
        },
    )
    gis_ref: Optional[GisRef] = field(
        default=None,
        metadata={
            "name": "GisRef",
            "type": "Element",
        },
    )
    gis_route: Optional[GisRouteType] = field(
        default=None,
        metadata={
            "name": "GisRoute",
            "type": "Element",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
        },
    )
    traffic_message: List[TrafficMessageType] = field(
        default_factory=list,
        metadata={
            "name": "TrafficMessage",
            "type": "Element",
        },
    )
    journey_status: Optional[JourneyStatusType] = field(
        default=None,
        metadata={
            "name": "JourneyStatus",
            "type": "Element",
        },
    )
    product: List[ProductType] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
        },
    )
    combined_product: List[CombinedProductType] = field(
        default_factory=list,
        metadata={
            "name": "CombinedProduct",
            "type": "Element",
        },
    )
    polyline: Optional[Polyline] = field(
        default=None,
        metadata={
            "name": "Polyline",
            "type": "Element",
        },
    )
    polyline_group: Optional[PolylineGroup] = field(
        default=None,
        metadata={
            "name": "PolylineGroup",
            "type": "Element",
        },
    )
    stops: Optional[Stops] = field(
        default=None,
        metadata={
            "name": "Stops",
            "type": "Element",
        },
    )
    service_days: List[ServiceDays] = field(
        default_factory=list,
        metadata={
            "name": "ServiceDays",
            "type": "Element",
        },
    )
    journey_detail: Optional[JourneyDetail] = field(
        default=None,
        metadata={
            "name": "JourneyDetail",
            "type": "Element",
        },
    )
    parallel_journey: List[JourneyType] = field(
        default_factory=list,
        metadata={
            "name": "ParallelJourney",
            "type": "Element",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
        },
    )
    referenced_journey: List[ReferencedJourneyType] = field(
        default_factory=list,
        metadata={
            "name": "referencedJourney",
            "type": "Element",
        },
    )
    id: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    idx: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    add_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "addName",
            "type": "Attribute",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    category: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    cancelled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    part_cancelled: bool = field(
        default=False,
        metadata={
            "name": "partCancelled",
            "type": "Attribute",
        },
    )
    reachable: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    redirected: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    direction: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    direction_flag: Optional[str] = field(
        default=None,
        metadata={
            "name": "directionFlag",
            "type": "Attribute",
        },
    )
    duration: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dist: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hide: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    ps_ctx_arrive_earlier: Optional[str] = field(
        default=None,
        metadata={
            "name": "psCtxArriveEarlier",
            "type": "Attribute",
        },
    )
    ps_ctx_depart_later: Optional[str] = field(
        default=None,
        metadata={
            "name": "psCtxDepartLater",
            "type": "Attribute",
        },
    )
    rec_state: Optional[ReconstructionStateType] = field(
        default=None,
        metadata={
            "name": "recState",
            "type": "Attribute",
        },
    )
    change_assured: Optional[bool] = field(
        default=None,
        metadata={
            "name": "changeAssured",
            "type": "Attribute",
        },
    )
    uncertain_delay: bool = field(
        default=False,
        metadata={
            "name": "uncertainDelay",
            "type": "Attribute",
        },
    )


@dataclass
class TrackMatchJourneyDetail:
    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail: Optional[JourneyDetail] = field(
        default=None,
        metadata={
            "name": "JourneyDetail",
            "type": "Element",
        },
    )
    match_time_span_begin: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "matchTimeSpanBegin",
            "type": "Attribute",
        },
    )
    match_time_span_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "matchTimeSpanEnd",
            "type": "Attribute",
        },
    )


@dataclass
class JourneyDetailGroupList(CommonResponseType):
    """
    A list of grouped detailed journeys.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    journey_detail_group: List[JourneyDetailGroup] = field(
        default_factory=list,
        metadata={
            "name": "JourneyDetailGroup",
            "type": "Element",
        },
    )


@dataclass
class JourneyTrackMatchResult:
    match_quality: Optional[MatchQualityType] = field(
        default=None,
        metadata={
            "name": "MatchQuality",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    track_match_journey_detail: List[TrackMatchJourneyDetail] = field(
        default_factory=list,
        metadata={
            "name": "TrackMatchJourneyDetail",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    diagnostics: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "Diagnostics",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    algorithm: Optional[MatchAlgorithmType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    deviation: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class LegList:
    """
    The element LegList contains all legs of the computed trip.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    leg: List[Leg] = field(
        default_factory=list,
        metadata={
            "name": "Leg",
            "type": "Element",
        },
    )


@dataclass
class MultiBoard:
    """
    Lists multiple arrival or departure boards.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    arrival_board: List[ArrivalBoard] = field(
        default_factory=list,
        metadata={
            "name": "ArrivalBoard",
            "type": "Element",
            "sequence": 1,
        },
    )
    departure_board: List[DepartureBoard] = field(
        default_factory=list,
        metadata={
            "name": "DepartureBoard",
            "type": "Element",
            "sequence": 1,
        },
    )


@dataclass
class JourneyTrackMatch(CommonResponseType):
    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    match_result: List[JourneyTrackMatchResult] = field(
        default_factory=list,
        metadata={
            "name": "MatchResult",
            "type": "Element",
        },
    )
    diagnostics: List[Kvtype] = field(
        default_factory=list,
        metadata={
            "name": "Diagnostics",
            "type": "Element",
        },
    )


@dataclass
class TripType:
    """
    :ivar origin:
    :ivar destination:
    :ivar messages:
    :ivar notes:
    :ivar eco:
    :ivar eco_cmp:
    :ivar service_days:
    :ivar freq:
    :ivar leg_list: The element LegList contains all legs of the
        computed trip.
    :ivar tariff_result:
    :ivar calculation:
    :ivar occupancy:
    :ivar reliability: Reliability of the connection or potential
        alternative connections that will indicate the likelihood of
        getting the user to the requested destination in time. Used in
        the time machine feature
    :ivar trip_status:
    :ivar via: Contains via locations from the request in the order they
        were initially specified.
    :ivar alternative: The type indicates whether this is an original
        connection or an realtime alternative.
    :ivar has_alternative: The type indicates whether this connection
        has an alternative or not.
    :ivar individual_change_times: The type indicates whether this trip
        is based on individual change times (true) or not (false).
        Default is false.
    :ivar valid: The state indicates if the trip is still possible to
        ride based on the current realtime situation.
    :ivar idx: The index of this trip in the result list. It corresponds
        to date and time order ascending; unique within the composite
        TripResponse.
    :ivar trip_id: The trip id of this trip in the result list.
    :ivar ctx_recon: Information for trip reconstruction.
    :ivar duration: The duration of the trip.
    :ivar rt_duration: Realtime duration of the trip.
    :ivar return_value: true: indicates the trip is a return journey.
    :ivar eco_url: Contains a precalculated url.
    :ivar checksum: Checksum of the trip to filter same results on
        client side after scroll requests.
    :ivar transfer_count: Count of transfers.
    :ivar combined_count: Count of packed trips in case of interval
        result packing requested.
    :ivar combined_min_duration: Shortest duration of packed trip.
    """

    origin: Optional[Origin] = field(
        default=None,
        metadata={
            "name": "Origin",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    destination: Optional[Destination] = field(
        default=None,
        metadata={
            "name": "Destination",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    messages: Optional[Messages] = field(
        default=None,
        metadata={
            "name": "Messages",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    eco: Optional[EcoType] = field(
        default=None,
        metadata={
            "name": "Eco",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    eco_cmp: List[EcoType] = field(
        default_factory=list,
        metadata={
            "name": "EcoCmp",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    service_days: List[ServiceDays] = field(
        default_factory=list,
        metadata={
            "name": "ServiceDays",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    freq: Optional[FreqType] = field(
        default=None,
        metadata={
            "name": "Freq",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    leg_list: Optional[LegList] = field(
        default=None,
        metadata={
            "name": "LegList",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    tariff_result: Optional[TariffResult] = field(
        default=None,
        metadata={
            "name": "TariffResult",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    calculation: Optional[CalculationType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    occupancy: List[OccupancyType] = field(
        default_factory=list,
        metadata={
            "name": "Occupancy",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    reliability: Optional[ConnectionReliabilityType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    trip_status: Optional[TripStatusType] = field(
        default=None,
        metadata={
            "name": "TripStatus",
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    via: List[StopType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://hacon.de/hafas/proxy/hafas-proxy",
        },
    )
    alternative: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    has_alternative: bool = field(
        default=False,
        metadata={
            "name": "hasAlternative",
            "type": "Attribute",
        },
    )
    individual_change_times: bool = field(
        default=False,
        metadata={
            "name": "individualChangeTimes",
            "type": "Attribute",
        },
    )
    valid: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    idx: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    trip_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "tripId",
            "type": "Attribute",
        },
    )
    ctx_recon: Optional[str] = field(
        default=None,
        metadata={
            "name": "ctxRecon",
            "type": "Attribute",
        },
    )
    duration: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rt_duration: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "rtDuration",
            "type": "Attribute",
        },
    )
    return_value: bool = field(
        default=False,
        metadata={
            "name": "return",
            "type": "Attribute",
        },
    )
    eco_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "ecoUrl",
            "type": "Attribute",
        },
    )
    checksum: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    transfer_count: int = field(
        default=0,
        metadata={
            "name": "transferCount",
            "type": "Attribute",
        },
    )
    combined_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "combinedCount",
            "type": "Attribute",
        },
    )
    combined_min_duration: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "combinedMinDuration",
            "type": "Attribute",
        },
    )


@dataclass
class Trip(TripType):
    """
    The element Trip contains a leg list of the computed trip.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"


@dataclass
class TripList(CommonResponseType):
    """The trip list contains all found trips of that trip request.

    If a major error occured during the trip request, then the
    attributes errorCode and errorText are filled and no Trip is
    available.

    :ivar trip:
    :ivar pricing:
    :ivar sot_context:
    :ivar result_status:
    :ivar scr_b: The context for scroll request backward. Set the
        context attribute in a Trip request for finding earlier
        connections.
    :ivar scr_f: The context for scroll request forward. Set the context
        attribute in a Trip request for finding later connections.
    :ivar scr_return_b: The context for scroll request backward for
        returning trips. Set the context attribute in a Trip request for
        finding earlier connections.
    :ivar scr_return_f: The context for scroll request forward for
        returning trips. Set the context attribute in a Trip request for
        finding later connections.
    """

    class Meta:
        namespace = "http://hacon.de/hafas/proxy/hafas-proxy"

    trip: List[Trip] = field(
        default_factory=list,
        metadata={
            "name": "Trip",
            "type": "Element",
        },
    )
    pricing: List[PricingType] = field(
        default_factory=list,
        metadata={
            "name": "Pricing",
            "type": "Element",
        },
    )
    sot_context: Optional[SotContextType] = field(
        default=None,
        metadata={
            "name": "SotContext",
            "type": "Element",
        },
    )
    result_status: Optional[ResultStatusType] = field(
        default=None,
        metadata={
            "name": "ResultStatus",
            "type": "Element",
        },
    )
    scr_b: Optional[str] = field(
        default=None,
        metadata={
            "name": "scrB",
            "type": "Attribute",
        },
    )
    scr_f: Optional[str] = field(
        default=None,
        metadata={
            "name": "scrF",
            "type": "Attribute",
        },
    )
    scr_return_b: Optional[str] = field(
        default=None,
        metadata={
            "name": "scrReturnB",
            "type": "Attribute",
        },
    )
    scr_return_f: Optional[str] = field(
        default=None,
        metadata={
            "name": "scrReturnF",
            "type": "Attribute",
        },
    )
