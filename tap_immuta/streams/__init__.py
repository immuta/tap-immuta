from tap_immuta.streams.audit import AuditStream
from tap_immuta.streams.data_source import *
from tap_immuta.streams.global_policy import GlobalPolicyStream
from tap_immuta.streams.group import GroupStream
from tap_immuta.streams.project import ProjectStream
from tap_immuta.streams.purpose import PurposeStream
from tap_immuta.streams.tag import TagStream
from tap_immuta.streams.user import UserStream

AVAILABLE_STREAMS = [
    AuditStream,
    DataSourceStream,
    DataSourceSubscriptionStream,
    DataSourceDictionaryStream,
    GlobalPolicyStream,
    GroupStream,
    ProjectStream,
    PurposeStream,
    TagStream,
    UserStream
]

__all__ = [
    "AuditStream",
    "DataSourceStream",
    "DataSourceSubscriptionStream",
    "GlobalPolicyStream",
    "GroupStream",
    "ProjectStream",
    "PurposeStream",
    "TagStream",
    "UserStream"
]