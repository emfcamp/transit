from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1"


class AlertAudienceType(Enum):
    """
    Alert Audience Data Type.
    """

    CUSTOMER = "Customer"
    STAFF = "Staff"
    OPERATIONS = "Operations"


@dataclass
class AlertService:
    """
    TODO.

    :ivar location: TODO
    :ivar rid: TODO
    :ivar uid: TODO
    :ivar ssd: TODO
    """

    location: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "min_occurs": 1,
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "name": "RID",
            "type": "Attribute",
            "max_length": 16,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "name": "UID",
            "type": "Attribute",
            "length": 6,
        },
    )
    ssd: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "SSD",
            "type": "Attribute",
        },
    )


class AlertType(Enum):
    """
    Alert Type Data Type.
    """

    NORMAL = "Normal"
    FORCED = "Forced"


@dataclass
class AlertServices:
    """
    A list of services to which the alert applies.

    :ivar alert_service: TODO
    """

    alert_service: List[AlertService] = field(
        default_factory=list,
        metadata={
            "name": "AlertService",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
        },
    )


@dataclass
class TrainAlert:
    """
    Train Alert.

    :ivar alert_id: TODO
    :ivar alert_services: TODO
    :ivar send_alert_by_sms: TODO
    :ivar send_alert_by_email: TODO
    :ivar send_alert_by_twitter: TODO
    :ivar source: TODO
    :ivar alert_text: TODO
    :ivar audience: TODO
    :ivar alert_type: TODO
    :ivar copied_from_alert_id: TODO
    :ivar copied_from_source: TODO
    """

    alert_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AlertID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    alert_services: Optional[AlertServices] = field(
        default=None,
        metadata={
            "name": "AlertServices",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    send_alert_by_sms: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SendAlertBySMS",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    send_alert_by_email: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SendAlertByEmail",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    send_alert_by_twitter: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SendAlertByTwitter",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    source: Optional[str] = field(
        default=None,
        metadata={
            "name": "Source",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    alert_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "AlertText",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    audience: Optional[AlertAudienceType] = field(
        default=None,
        metadata={
            "name": "Audience",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    alert_type: Optional[AlertType] = field(
        default=None,
        metadata={
            "name": "AlertType",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
            "required": True,
        },
    )
    copied_from_alert_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CopiedFromAlertID",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
        },
    )
    copied_from_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "CopiedFromSource",
            "type": "Element",
            "namespace": "http://www.thalesgroup.com/rtti/PushPort/TrainAlerts/v1",
        },
    )
