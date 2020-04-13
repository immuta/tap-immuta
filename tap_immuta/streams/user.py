import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class UserStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'user'
    KEY_PROPERTIES = ['username']

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/bim/user"