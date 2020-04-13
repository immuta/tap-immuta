import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class AuditStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'audit'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/audit"