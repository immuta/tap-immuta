"""Stream class for tap-immuta."""

import math

from typing import Any, Dict, Optional, Union, List, Iterable, cast
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_immuta import schemas
from tap_immuta.client import ImmutaStream


class ParentBaseStream(ImmutaStream):
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

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
        params = {"size": self._page_size, "offset": 1}
        if next_page_token:
            params["offset"] = next_page_token
        return params


class DataSourceStream(ParentBaseStream):
    name = "data_source"
    path = "/dataSource"
    primary_keys = ["id"]
    schema = schemas.data_source

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {
                "data_source_id": row["id"],
                "connectionString": row["connectionString"],
            }
            yield (row, child_context)

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Append data source and connection string to record."""
        # Get additional data from direct endpoint
        prepared_request = self.prepare_request(context=context, next_page_token=None)
        prepared_request.url = f"{self.url_base}/dataSource/{row['id']}"
        prepared_request.params = {}
        response = self._request_with_backoff(prepared_request, context)

        # Set emitted record to be the detailed record
        record = response.json()
        record["connectionString"] = row["connectionString"]
        return record


class DataSourceDictionaryStream(ImmutaStream):
    name = "data_source_dictionary"
    path = "/dictionary/{data_source_id}"
    primary_keys = ["dataSource"]
    parent_stream_type = DataSourceStream
    ignore_parent_replication_keys = True

    schema = schemas.data_source_dictionary


class DataSourceSubscriptionStream(ImmutaStream):
    name = "data_source_subscription"
    path = "/dataSource/{data_source_id}/access"
    primary_keys = ["data_source_id", "profile"]
    records_jsonpath = "$.users[*]"
    parent_stream_type = DataSourceStream
    ignore_parent_replication_keys = True

    schema = schemas.data_source_subscription


class GlobalPolicyStream(ImmutaStream):
    name = "global_policy"
    path = "/policy/global"
    primary_keys = ["id"]

    schema = schemas.global_policy


class GroupStream(ImmutaStream):
    name = "group"
    path = "/bim/group"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    schema = schemas.group


class IamStream(ImmutaStream):
    name = "iam"
    path = "/bim/iam"
    primary_keys = ["id"]

    schema = schemas.iam


class ProjectStream(ParentBaseStream):
    name = "project"
    path = "/project"
    primary_keys = ["id"]

    schema = schemas.project

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {
                "project_id": row["id"],
            }
            yield (row, child_context)

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Append data source and connection string to record."""
        # Get additional data from direct endpoint
        prepared_request = self.prepare_request(context=context, next_page_token=None)
        prepared_request.url = f"{self.url_base}/project/{row['id']}"
        prepared_request.params = {}
        response = self._request_with_backoff(prepared_request, context)

        # Set emitted record to be the detailed record
        record = response.json()
        return record


class ProjectDataSourceStream(ImmutaStream):
    name = "project_data_source"
    path = "/project/{project_id}/dataSources"
    primary_keys = ["project_id", "dataSourceId"]
    records_jsonpath = "$.dataSources[*]"
    parent_stream_type = ProjectStream
    ignore_parent_replication_keys = True

    schema = schemas.project_data_source


class ProjectMemberStream(ImmutaStream):
    name = "project_member"
    path = "/project/{project_id}/members"
    primary_keys = ["project_id", "profile"]
    records_jsonpath = "$.members[*]"
    parent_stream_type = ProjectStream
    ignore_parent_replication_keys = True

    schema = schemas.project_member


class PurposeStream(ImmutaStream):
    name = "purpose"
    path = "/governance/purpose"
    primary_keys = ["id"]
    records_jsonpath = "$.purposes[*]"

    schema = schemas.purpose


class TagStream(ImmutaStream):
    name = "tag"
    path = "/tag"
    primary_keys = ["id"]

    schema = schemas.tag


class UserStream(ImmutaStream):
    name = "user"
    path = "/bim/user"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    schema = schemas.user

class AuditStream(ImmutaStream):
    name = "audit"
    path = "/bim/user"
    primary_keys = ["id"]
    records_jsonpath = "$.hits[*]"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["Size"] = self._page_size
        params["RecordType"] = [
            t for t in schemas.AUDIT_RECORD_TYPES if t != 'auditQuery'
        ]
        params["MinDate"] = self.get_starting_timestamp()
        params["SortField"] = "DateTime"
        params["SortOrder"] = "asc"
    schema = schemas.user