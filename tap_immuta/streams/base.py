import inspect
import math
import os.path
import pytz
import singer
import singer.utils
import singer.metrics

from datetime import timedelta, datetime

from tap_immuta.config import get_config_start_date
from tap_immuta.streams import cache as stream_cache
from tap_immuta.state import incorporate, save_state, \
    get_last_record_value_for_table


LOGGER = singer.get_logger()


class BaseStream:
    # GLOBAL PROPERTIES
    TABLE = None
    KEY_PROPERTIES = ["id"]
    RESPONSE_RESULT_KEY = None
    API_METHOD = 'GET'
    REQUIRES = []
    CACHE_RESULTS = False
    path = ""

    def __init__(self, config, state, catalog, client):
        self.config = config
        self.state = state
        self.catalog = catalog
        self.client = client
        self.substreams = []

    def get_url_base(self):
        return f"{self.config['immuta_host']}"

    def get_url(self):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        return f"{base}{self.path}"

    def get_params(self, page=0):
        return {"size": 100, "offset": page}

    def get_class_path(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def load_schema_by_name(self, name):
        return singer.utils.load_json(
            os.path.normpath(
                os.path.join(
                    self.get_class_path(),
                    '../schemas/{}.json'.format(name))))

    def get_schema(self):
        return self.load_schema_by_name(self.TABLE)

    def get_stream_data(self, result):
        """Given a result set, return the data
        to be persisted for this stream.
        """
        if not isinstance(result, list):
            raise TypeError(f"Result must be list. Got: {result}")

        return [
            self.transform_record(record)
            for record in result
        ]
        
    @classmethod
    def requirements_met(cls, catalog):
        selected_streams = [
            s.stream for s in catalog.streams if is_selected(s)
        ]

        return set(cls.REQUIRES).issubset(selected_streams)

    @classmethod
    def matches_catalog(cls, stream_catalog):
        return stream_catalog.stream == cls.TABLE

    def generate_catalog(self, selected_by_default=True):
        schema = self.get_schema()
        mdata = singer.metadata.new()

        mdata = singer.metadata.write(mdata, (), "inclusion", "available")
        mdata = singer.metadata.write(
            mdata, (), "selected-by-default", selected_by_default
        )

        for field_name in schema.get("properties").keys():
            inclusion = "available"

            if field_name in self.KEY_PROPERTIES:
                inclusion = "automatic"

            mdata = singer.metadata.write(
                mdata, ("properties", field_name), "inclusion", inclusion
            )
            mdata = singer.metadata.write(
                mdata,
                ("properties", field_name),
                "selected-by-default",
                selected_by_default,
            )

        return [
            {
                "tap_stream_id": self.TABLE,
                "stream": self.TABLE,
                "key_properties": self.KEY_PROPERTIES,
                "schema": self.get_schema(),
                "metadata": singer.metadata.to_list(mdata),
            }
        ]


    def transform_record(self, record):
        with singer.Transformer() as tx:
            metadata = {}

            if not isinstance(record, dict):
                raise TypeError(f'Record must be dict. got: {record}')

            if self.catalog.metadata is not None:
                metadata = singer.metadata.to_map(self.catalog.metadata)

            return tx.transform(
                    record,
                    self.catalog.schema.to_dict(),
                    metadata)

    def get_catalog_keys(self):
        return list(self.catalog.schema.properties.keys())

    def write_schema(self):
        singer.write_schema(
            self.catalog.stream,
            self.catalog.schema.to_dict(),
            key_properties=self.catalog.key_properties)

    def sync(self):
        LOGGER.info('Syncing stream {} with {}'
                    .format(self.catalog.tap_stream_id,
                            self.__class__.__name__))

        self.write_schema()

        return self.sync_data()

    def sync_data(self):
        table = self.TABLE

        LOGGER.info("Syncing data for {}".format(table))

        url = self.get_url()
        resources = self.sync_paginated(url)

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state

    def sync_paginated(self, url):
        table = self.TABLE
        _next = True
        page = 0
        params = self.get_params(page) 

        all_resources = []
        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)

            # Streams where the result contains a record list under a key
            if isinstance(result, dict) and self.RESPONSE_RESULT_KEY is not None:
                LOGGER.debug(f"Retrieving records from response field: {self.RESPONSE_RESULT_KEY}")
                records = result[self.RESPONSE_RESULT_KEY]
                data = self.get_stream_data(records)
                total_records = int(result.get("count"))

            # API directly returns record list
            elif isinstance(result, list):
                LOGGER.debug(f"Retrieving records from response list")
                data = self.get_stream_data(result)
                total_records = len(data)

            # API returns a single record
            else:
                LOGGER.debug("Using response as individual record.")
                data = self.get_stream_data([result])
                total_records = len(data)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, data)
                counter.increment(len(data))
                all_resources.extend(data)

            LOGGER.info("Synced page %s for %s (%s records)", 
                page, self.TABLE, len(all_resources))
            if len(all_resources) == total_records:
                _next = None
            else:
                page += 1
                params = self.get_params(page) 
        return all_resources


def is_selected(stream_catalog):
    metadata = singer.metadata.to_map(stream_catalog.metadata)
    stream_metadata = metadata.get((), {})

    inclusion = stream_metadata.get('inclusion')

    if stream_metadata.get('selected') is not None:
        selected = stream_metadata.get('selected')
    else:
        selected = stream_metadata.get('selected-by-default')

    if inclusion == 'unsupported':
        return False

    elif selected is not None:
        return selected

    return inclusion == 'automatic'

