from singer_sdk.streams import RESTStream
from tap_immuta.auth import ImmutaAuthenticator


class ImmutaStream(RESTStream):
    """Immuta stream class."""

    _page_size = 200

    @property
    def authenticator(self):
        return ImmutaAuthenticator.create_for_stream(self)

    @property
    def url_base(self) -> str:
        return self.config["hostname"]
