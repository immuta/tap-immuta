import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class DataSourceSubscriptionStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'data_source'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    self.data_source_ids = self.make

    @property
    def path_list(self):
        return f"/dataSource/1/access"
        