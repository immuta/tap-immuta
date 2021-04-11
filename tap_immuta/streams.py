"""Stream class for tap-immuta."""

import requests

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from singer_sdk.streams import RESTStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ImmutaStream(RESTStream):
    """Immuta stream class."""

    response_result_key = None

    @property
    def http_headers(self) -> dict:
        return {"Authorization": self.config.get("api_key")}

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["immuta_host"]

    def get_url_params(
        self, partition: Optional[dict], next_page_token: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        If paging is supported, developers may override this method with specific paging
        logic.
        """
        params = {}
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        if self.response_result_key:
            resp_json = resp_json.get(self.response_result_key, {})
        if isinstance(resp_json, dict):
            yield resp_json
        else:
            for row in resp_json:
                yield row


class ChildStream(ImmutaStream):
    @property
    def partitions(self) -> List[dict]:
        """Return a list of partition key dicts (if applicable), otherwise None."""
        if "{data_source_id}" in self.path:
            data_source_list = self._get_all_data_source_ids()
            return [{"data_source_id": ds["id"], "connectionString": ds["connectionString"]} for ds in data_source_list]
        if "{project_id}" in self.path:
            project_list = self._get_all_project_ids()
            return [{"project_id": id} for id in project_list]
        raise ValueError(
            "Could not detect partition type for Gitlab stream "
            f"'{self.name}' ({self.path}). "
        )

    def _get_all_data_source_ids(self):
        page = 0
        counter = 99999
        url = f"{self.url_base}/dataSource"
        data_source_data = []
        while len(data_source_data) < counter:
            params = {"offset": page, "size": 2000}
            response = self._requests_session.get(
                url, headers=self.http_headers, params=params
            ).json()
            for ii in response["hits"]:
                details = {
                    "id": ii.get("id"),
                    "connectionString": ii.get("connectionString"),
                }
                data_source_data.append(details)
            page += 1
            counter = response["count"]
        return data_source_data

    def _get_all_project_ids(self):
        page = 0
        counter = 99999
        url = f"{self.url_base}/project"
        project_list = []
        while len(project_list) < counter:
            params = {"offset": page, "size": 200}
            response = self._requests_session.get(
                url, headers=self.http_headers, params=params
            ).json()
            project_list.extend([ii.get("id") for ii in response["hits"]])
            page += 1
            counter = response["count"]
        return project_list

    def post_process(self, row: dict, partition: Optional[dict] = None) -> dict:
        """Append the partition keys to the record."""
        for ii in partition.keys():
            row[ii] = partition[ii]
        return row


class DataSourceStream(ChildStream):
    name = "data_source"
    path = "/dataSource/{data_source_id}"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "data_source.json"


class DataSourceDictionaryStream(ChildStream):
    name = "data_source_dictionary"
    path = "/dictionary/{data_source_id}"
    primary_keys = ["dataSource"]

    schema_filepath = SCHEMAS_DIR / "data_source_dictionary.json"


class DataSourceSubscriptionStream(ChildStream):
    name = "data_source_subscription"
    path = "/dataSource/{data_source_id}/access"
    primary_keys = ["data_source_id", "profile"]
    response_result_key = "users"

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
    response_result_key = "hits"

    schema_filepath = SCHEMAS_DIR / "group.json"


class IamStream(ImmutaStream):
    name = "iam"
    path = "/bim/iam"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "iam.json"


class ProjectStream(ChildStream):
    name = "project"
    path = "/project/{project_id}"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "project.json"


class ProjectDataSourceStream(ChildStream):
    name = "project_data_source"
    path = "/project/{project_id}/dataSources"
    primary_keys = ["project_id", "dataSourceId"]
    response_result_key = "dataSources"

    schema_filepath = SCHEMAS_DIR / "project_data_source.json"


class ProjectMemberStream(ChildStream):
    name = "project_member"
    path = "/project/{project_id}/members"
    primary_keys = ["project_id", "profile"]
    response_result_key = "members"

    schema_filepath = SCHEMAS_DIR / "project_member.json"


class PurposeStream(ImmutaStream):
    name = "purpose"
    path = "/governance/purpose"
    primary_keys = ["id"]
    response_result_key = "purposes"

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
    response_result_key = "hits"

    schema_filepath = SCHEMAS_DIR / "user.json"
