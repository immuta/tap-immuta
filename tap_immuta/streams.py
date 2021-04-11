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


class GlobalPolicyStream(ImmutaStream):
    name = "global_policy"
    path = "/policy/global"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "group.json"


class GroupStream(ImmutaStream):
    name = "group"
    path = "/bim/group"
    primary_keys = ["id"]
    response_result_key = "hits"

    schema_filepath = SCHEMAS_DIR / "group.json"


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
