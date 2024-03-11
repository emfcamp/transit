from dataclasses import dataclass, field
from typing import Optional

from darwin.push_port.rtti_pptfilter_v1 import FilterTiplocs
from darwin.push_port.rtti_pptrequest_td_v1 import RequestTd
from darwin.push_port.rtti_pptstatus_v1 import (
    Ppconnect,
    PpreqVersion,
    Ppstatus,
)

__NAMESPACE__ = "http://thalesgroup.com/RTTI/PushPortSetup/root_1"


@dataclass
class PpsetupReq:
    """
    Definition of request messages from clients.
    """

    class Meta:
        name = "PPSetupReq"
        namespace = "http://thalesgroup.com/RTTI/PushPortSetup/root_1"

    ppreq_version: Optional[PpreqVersion] = field(
        default=None,
        metadata={
            "name": "PPReqVersion",
            "type": "Element",
            "namespace": "http://thalesgroup.com/RTTI/PushPortStatus/root_1",
        },
    )
    ppconnect: Optional[Ppconnect] = field(
        default=None,
        metadata={
            "name": "PPConnect",
            "type": "Element",
            "namespace": "http://thalesgroup.com/RTTI/PushPortStatus/root_1",
        },
    )
    filter_tiplocs: Optional[FilterTiplocs] = field(
        default=None,
        metadata={
            "name": "FilterTiplocs",
            "type": "Element",
            "namespace": "http://thalesgroup.com/RTTI/PushPortFilter/root_1",
        },
    )
    request_td: Optional[RequestTd] = field(
        default=None,
        metadata={
            "name": "RequestTD",
            "type": "Element",
            "namespace": "http://thalesgroup.com/RTTI/PushPortRequestTD/root_1",
        },
    )
    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class PpsetupResp:
    """
    Definition of response messages to clients.
    """

    class Meta:
        name = "PPSetupResp"
        namespace = "http://thalesgroup.com/RTTI/PushPortSetup/root_1"

    ppstatus: Optional[Ppstatus] = field(
        default=None,
        metadata={
            "name": "PPStatus",
            "type": "Element",
            "namespace": "http://thalesgroup.com/RTTI/PushPortStatus/root_1",
        },
    )
    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
