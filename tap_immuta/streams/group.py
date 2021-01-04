import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class GroupStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'group'
    KEY_PROPERTIES = ['id']
    RESPONSE_RESULT_KEY = "hits"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/bim/group"