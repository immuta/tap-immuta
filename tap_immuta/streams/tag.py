import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class TagStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'tag'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/tag"

    def get_params(self, page=1):
        return {}