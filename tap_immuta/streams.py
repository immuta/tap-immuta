"""Stream class for tap-immuta."""

import requests
import copy
import math

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable, cast
from singer_sdk.streams import RESTStream
from singer_sdk import typing as th  # JSON Schema typing helpers


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ImmutaStream(RESTStream):
    """Immuta stream class."""
    _page_size = 200

    @property
    def http_headers(self) -> dict:
        return {"Authorization": self.config.get("api_key")}

    @property
    def url_base(self) -> str:
        return self.config["immuta_host"]


class ParentBaseStream(ImmutaStream):
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    @property
    def selected(self):
        "This is a utility stream that should not be selected."
        return False

    def get_next_page_token(self, response, previous_token):
        """
        Return a token for identifying next page or None if no more pages.
        The offset is the number of projects that should be skipped (not the page).
        """
        current_page = (previous_token or 0) / self._page_size
        total_pages = math.ceil(response.json()["count"] / self._page_size)
        self.logger.info(f"Traversed page {current_page} of {total_pages}.")
        if current_page < total_pages:
            next_page_token = (current_page + 1) * self._page_size
            self.logger.debug(f"Next page token retrieved: {next_page_token}")
            return next_page_token
        return None

    def get_url_params(self, context, next_page_token):
        """Return a dictionary of values to be used in URL parameterization."""
        params = {
            "size": self._page_size,
            "offset": 1
        }
        if next_page_token:
            params["offset"] = next_page_token
        return params


class DataSourceBaseStream(ParentBaseStream):
    name = "data_source_base"
    path = "/dataSource"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("connectionString", th.StringType)
    ).to_dict()

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {
                "data_source_id": row["id"],
                "connectionString": row["connectionString"]
            }
            yield (row, child_context)


class ProjectBaseStream(ParentBaseStream):
    name = "project_base"
    path = "/project"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
    ).to_dict()

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {"project_id": row["id"]}
            yield (row, child_context)


class DataSourceStream(ImmutaStream):
    name = "data_source"
    path = "/dataSource/{data_source_id}"
    primary_keys = ["id"]
    parent_stream_type = DataSourceBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "data_source.json"

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Append data source and connection string to record."""
        row["id"] = context["data_source_id"]
        row["connection_string"] = context["connectionString"]
        return row


class DataSourceDictionaryStream(ImmutaStream):
    name = "data_source_dictionary"
    path = "/dictionary/{data_source_id}"
    primary_keys = ["dataSource"]
    parent_stream_type = DataSourceBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "data_source_dictionary.json"


class DataSourceSubscriptionStream(ImmutaStream):
    name = "data_source_subscription"
    path = "/dataSource/{data_source_id}/access"
    primary_keys = ["data_source_id", "profile"]
    records_jsonpath = "$.users[*]"
    parent_stream_type = DataSourceBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "data_source_subscription.json"


class GlobalPolicyStream(ImmutaStream):
    name = "global_policy"
    path = "/policy/global"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "global_policy.json"


class GroupStream(ImmutaStream):
    name = "group"
    path = "/bim/group"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    schema_filepath = SCHEMAS_DIR / "group.json"


class IamStream(ImmutaStream):
    name = "iam"
    path = "/bim/iam"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "iam.json"


class ProjectStream(ImmutaStream):
    name = "project"
    path = "/project/{project_id}"
    primary_keys = ["id"]
    parent_stream_type = ProjectBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "project.json"


class ProjectDataSourceStream(ImmutaStream):
    name = "project_data_source"
    path = "/project/{project_id}/dataSources"
    primary_keys = ["project_id", "dataSourceId"]
    records_jsonpath = "$.dataSources[*]"
    parent_stream_type = ProjectBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "project_data_source.json"


class ProjectMemberStream(ImmutaStream):
    name = "project_member"
    path = "/project/{project_id}/members"
    primary_keys = ["project_id", "profile"]
    records_jsonpath = "$.members[*]"
    parent_stream_type = ProjectBaseStream
    ignore_parent_replication_keys = True

    schema_filepath = SCHEMAS_DIR / "project_member.json"


class PurposeStream(ImmutaStream):
    name = "purpose"
    path = "/governance/purpose"
    primary_keys = ["id"]
    records_jsonpath = "$.purposes[*]"

    schema_filepath = SCHEMAS_DIR / "purpose.json"


class TagStream(ImmutaStream):
    name = "tag"
    path = "/tag"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "tag.json"


class UserStream(ImmutaStream):
    name = "user"
    path = "/bim/user"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    schema_filepath = SCHEMAS_DIR / "user.json"
