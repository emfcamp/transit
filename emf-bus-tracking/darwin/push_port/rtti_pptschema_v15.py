from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from darwin.push_port.rtti_pptalarms_v1 import Rttialarm
from darwin.push_port.rtti_pptforecasts_v3 import Ts
from darwin.push_port.rtti_pptformations_v1 import (
    Loading,
    ScheduleFormations,
)
from darwin.push_port.rtti_pptschedules_v2 import (
    Association,
    DeactivatedSchedule,
)
from darwin.push_port.rtti_pptschedules_v3 import Schedule
from darwin.push_port.rtti_pptstation_messages_v1 import StationMessage
from darwin.push_port.rtti_pptstatus_v1 import StatusType
from darwin.push_port.rtti_ppttddata_v1 import TrackingId
from darwin.push_port.rtti_ppttrain_alerts_v1 import TrainAlert
from darwin.push_port.rtti_ppttrain_order_v1 import TrainOrder

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/v15"


@dataclass
class DataResponse:
    """
    :ivar schedule: Train Schedule
    :ivar deactivated: Notification that a Train Schedule is now
        deactivated in Darwin.
    :ivar association: Association between schedules
    :ivar schedule_formations: Train Formation
    :ivar ts: Train Status
    :ivar formation_loading: Train Loading
    :ivar ow: Darwin Workstation Station Message
    :ivar train_alert: Train Alert
    :ivar train_order: The order that trains are expected to call/pass a
        particular station platform
    :ivar tracking_id: Indicate a corrected Tracking ID (headcode) for a
        service in a TD berth.
    :ivar alarm: A Darwin alarm
    """

    schedule: List[Schedule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    deactivated: List[DeactivatedSchedule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    association: List[Association] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    schedule_formations: List[ScheduleFormations] = field(
        default_factory=list,
        metadata={
            "name": "scheduleFormations",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    ts: List[Ts] = field(
        default_factory=list,
        metadata={
            "name": "TS",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    formation_loading: List[Loading] = field(
        default_factory=list,
        metadata={
            "name": "formationLoading",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    ow: List[StationMessage] = field(
        default_factory=list,
        metadata={
            "name": "OW",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    train_alert: List[TrainAlert] = field(
        default_factory=list,
        metadata={
            "name": "trainAlert",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    train_order: List[TrainOrder] = field(
        default_factory=list,
        metadata={
            "name": "trainOrder",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    tracking_id: List[TrackingId] = field(
        default_factory=list,
        metadata={
            "name": "trackingID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )
    alarm: List[Rttialarm] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/v15",
        },
    )


@dataclass
class Pport:
    """
    Push Ports Schema.

    :ivar query_timetable: Query for the current timetable ID
    :ivar time_table_id: Response for the current timetable ID
    :ivar get_snapshot_req: Request a standard snapshot of current
        database
    :ivar get_full_snapshot_req: Request a full snapshot of current
        database
    :ivar snapshot_id: Defines an ID for recovering snapshot data via
        FTP
    :ivar start_update_req: Start sending available updates.
    :ivar stop_update_req: Stop sending available updates.
    :ivar failure_resp: Failure Response
    :ivar u_r: Update Response
    :ivar s_r: Snapshot Response
    :ivar ts: Local Timestamp
    :ivar version:
    """

    class Meta:
        namespace = "http://www.thalesgroup.com/rtti/PushPort/v15"

    query_timetable: Optional[object] = field(
        default=None,
        metadata={
            "name": "QueryTimetable",
            "type": "Element",
        },
    )
    time_table_id: Optional["Pport.TimeTableId"] = field(
        default=None,
        metadata={
            "name": "TimeTableId",
            "type": "Element",
        },
    )
    get_snapshot_req: Optional["Pport.GetSnapshotReq"] = field(
        default=None,
        metadata={
            "name": "GetSnapshotReq",
            "type": "Element",
        },
    )
    get_full_snapshot_req: Optional["Pport.GetFullSnapshotReq"] = field(
        default=None,
        metadata={
            "name": "GetFullSnapshotReq",
            "type": "Element",
        },
    )
    snapshot_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SnapshotId",
            "type": "Element",
            "max_length": 40,
        },
    )
    start_update_req: Optional[object] = field(
        default=None,
        metadata={
            "name": "StartUpdateReq",
            "type": "Element",
        },
    )
    stop_update_req: Optional[object] = field(
        default=None,
        metadata={
            "name": "StopUpdateReq",
            "type": "Element",
        },
    )
    failure_resp: Optional["Pport.FailureResp"] = field(
        default=None,
        metadata={
            "name": "FailureResp",
            "type": "Element",
        },
    )
    u_r: Optional["Pport.UR"] = field(
        default=None,
        metadata={
            "name": "uR",
            "type": "Element",
        },
    )
    s_r: Optional[DataResponse] = field(
        default=None,
        metadata={
            "name": "sR",
            "type": "Element",
        },
    )
    ts: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class TimeTableId:
        value: str = field(
            default="",
            metadata={
                "required": True,
                "length": 14,
            },
        )
        ttfile: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "min_length": 1,
                "max_length": 128,
            },
        )
        ttreffile: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "min_length": 1,
                "max_length": 128,
            },
        )

    @dataclass
    class GetSnapshotReq:
        """
        :ivar viaftp: If true, then resulting snapshot data is fetched
            by the client via FTP
        """

        viaftp: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class GetFullSnapshotReq:
        """
        :ivar viaftp: If true, then resulting snapshot data is fetched
            by the client via FTP
        """

        viaftp: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class FailureResp(StatusType):
        """
        :ivar request_source: The DCIS source that generated this update
        :ivar request_id: The DCISRequestID value provided by the
            originator of this update. Used in conjunction with the
            updateSource attribute to ensure uniqueness
        """

        request_source: Optional[str] = field(
            default=None,
            metadata={
                "name": "requestSource",
                "type": "Attribute",
                "length": 4,
            },
        )
        request_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "requestID",
                "type": "Attribute",
                "min_length": 1,
                "max_length": 16,
                "pattern": r"[-_A-Za-z0-9]{1,16}",
            },
        )

    @dataclass
    class UR(DataResponse):
        """
        :ivar update_origin: A string describing the type of system that
            originated this update, e.g. "CIS" or "Darwin".
        :ivar request_source: The source instance that generated this
            update, usually a CIS instance.
        :ivar request_id: The DCISRequestID value provided by the
            originator of this update. Used in conjunction with the
            requestSource attribute to ensure uniqueness
        """

        update_origin: Optional[str] = field(
            default=None,
            metadata={
                "name": "updateOrigin",
                "type": "Attribute",
            },
        )
        request_source: Optional[str] = field(
            default=None,
            metadata={
                "name": "requestSource",
                "type": "Attribute",
                "length": 4,
            },
        )
        request_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "requestID",
                "type": "Attribute",
                "min_length": 1,
                "max_length": 16,
                "pattern": r"[-_A-Za-z0-9]{1,16}",
            },
        )
