import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache
from tap_immuta.state import save_state


LOGGER = singer.get_logger()  # noqa


class DataSourceStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'data_source'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    def get_params(self, page):
        return {}

    def get_all_data_source_ids(self):
        page = 0
        counter = 9999
        url = f"{self.get_url_base()}/dataSource"
        data_source_data = []
        while len(data_source_data) < counter:
            params = {"offset": page, "size": 2000}
            response = self.client.make_request(url, "GET", params=params)
            data_source_data.extend([
                {
                    "id": ii.get("id"),
                    "connectionString": ii.get("connectionString")
                }
                for ii in response["hits"]
            ])
            page += 1
            counter = response["count"]
        LOGGER.info("Found %s Data Sources.", counter)
        return data_source_data

    def get_url(self, data_source_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/dataSource/{data_source_id}"
        return f"{base}{path}"

    def sync_data(self):
        table = self.TABLE

        data_source_list = self.get_all_data_source_ids()
        resources = list()
        for ds_data in data_source_list:
            additional_attributes = {"connectionString": ds_data["connectionString"]}
            url = self.get_url(ds_data["id"])
            LOGGER.info("Syncing data for %s %s at %s", table, ds_data["id"], url)
            resources.extend(self.sync_paginated(url, additional_attributes))

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state


class DataSourceSubscriptionStream(DataSourceStream):
    API_METHOD = 'GET'
    TABLE = 'data_source_subscription'
    KEY_PROPERTIES = ['data_source_id', 'profile']
    RESPONSE_RESULT_KEY="users"
    IS_SELECTED_BY_DEFAULT = True

    CACHE_RESULTS = True

    def get_params(self, page):
        return {}

    def get_url(self, data_source_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/dataSource/{data_source_id}/access"
        return f"{base}{path}"

    def sync_data(self):
        table = self.TABLE

        data_source_list = self.get_all_data_source_ids()
        resources = list()
        for ds_data in data_source_list:
            child_id = ds_data["id"]
            additional_attributes = {"data_source_id": child_id}
            url = self.get_url(child_id)
            LOGGER.info("Syncing data for %s %s at %s", table, child_id, url)
            results = self.sync_paginated(url, additional_attributes)
            resources.extend(results)

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state

class DataSourceDictionaryStream(DataSourceStream):
    API_METHOD = 'GET'
    TABLE = 'data_source_dictionary'
    KEY_PROPERTIES = ['dataSource']

    CACHE_RESULTS = True

    def get_url(self, data_source_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/dictionary/{data_source_id}"
        return f"{base}{path}"
