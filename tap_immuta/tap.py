"""Immuta tap class."""

from pathlib import Path
from typing import List

from singer_sdk import Tap, Stream
from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    IntegerType,
    NumberType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

from tap_immuta.streams import (
    ImmutaStream,
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

    config_jsonschema = PropertiesList(
        Property("immuta_host", StringType, required=True),
        Property("api_key", StringType, required=True),
        Property("start_date", DateTimeType),
        Property("user_agent", StringType, default="tap-immuta@immuta.com"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


# CLI Execution:

cli = TapImmuta.cli
