"""MySourceName Authentication."""


from singer_sdk.authenticators import SimpleAuthenticator


class ImmutaAuthenticator(SimpleAuthenticator):
    """Authenticator class for MySourceName."""

    @classmethod
    def create_for_stream(cls, stream) -> "ImmutaAuthenticator":
        return cls(
            stream=stream,
            auth_headers={
                {"Authorization": stream.config["api_key"]}
            }
        )
