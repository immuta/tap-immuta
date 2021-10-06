from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


class ImmutaStream(RESTStream):
    """Immuta stream class."""

    _page_size = 200

    @property
    def authenticator(self):
        return APIKeyAuthenticator.create_for_stream(
            self, key="Authorization", value=self.config["api_key"], location="header"
        )

    @property
    def url_base(self) -> str:
        return self.config["hostname"]
