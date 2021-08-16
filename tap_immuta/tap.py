"""Immuta tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th

from tap_immuta.streams import (
    DataSourceStream,
    DataSourceDictionaryStream,
    DataSourceSubscriptionStream,
    GlobalPolicyStream,
    GroupStream,
    IamStream,
    ProjectStream,
    ProjectDataSourceStream,
    ProjectMemberStream,
    PurposeStream,
    TagStream,
    UserStream,
)


STREAM_TYPES = [
    DataSourceStream,
    DataSourceDictionaryStream,
    DataSourceSubscriptionStream,
    GlobalPolicyStream,
    GroupStream,
    IamStream,
    ProjectStream,
    ProjectDataSourceStream,
    ProjectMemberStream,
    PurposeStream,
    TagStream,
    UserStream,
]


class TapImmuta(Tap):
    """Immuta tap class."""

    name = "tap-immuta"

    config_jsonschema = th.PropertiesList(
        th.Property("immuta_host", th.StringType, required=True),
        th.Property("api_key", th.StringType, required=True),
        th.Property("user_agent", th.StringType, default="tap-immuta"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


# CLI Execution:
cli = TapImmuta.cli
