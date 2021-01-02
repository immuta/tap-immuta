import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class PurposeStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'purpose'
    KEY_PROPERTIES = ['id']
    RESPONSE_RESULT_KEY = "purposes"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/governance/purpose"