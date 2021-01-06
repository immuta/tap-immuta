import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache
from tap_immuta.state import save_state


LOGGER = singer.get_logger()  # noqa


class ProjectStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'project'
    KEY_PROPERTIES = ['id']

    def get_params(self, page):
        return {}

    def get_all_project_ids(self):
        page = 0
        counter = 9999
        url = f"{self.get_url_base()}/project"
        id_list = []
        while len(id_list) < counter:
            params = {"offset": page, "size": 200}
            response = self.client.make_request(url, "GET", params=params)
            id_list.extend([ii.get("id") for ii in response["hits"]])
            page += 1
            counter = response["count"]
        LOGGER.info("Found %s Data Sources.", counter)
        return id_list

    def get_url(self, project_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/project/{project_id}"
        return f"{base}{path}"

    def sync_data(self):
        table = self.TABLE

        project_list = self.get_all_project_ids()
        resources = list()
        for child_id in project_list:
            url = self.get_url(child_id)
            LOGGER.info("Syncing data for %s %s at %s", table, child_id, url)
            resources.extend(self.sync_paginated(url))

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state


class ProjectMemberStream(ProjectStream):
    API_METHOD = 'GET'
    TABLE = 'project_member'
    KEY_PROPERTIES = ['project_id', 'subscriptionId']
    RESPONSE_RESULT_KEY = "members"
    IS_SELECTED_BY_DEFAULT = True

    CACHE_RESULTS = True

    def get_params(self, page=0):
        return {"size": 500, "offset": page}

    def get_url(self, project_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/project/{project_id}/members"
        return f"{base}{path}"

    def sync_data(self):
        table = self.TABLE

        project_list = self.get_all_project_ids()
        resources = list()
        for child_id in project_list:
            additional_attributes = {"project_id": child_id}
            url = self.get_url(child_id)
            LOGGER.info("Syncing data for %s %s at %s", table, child_id, url)
            resources.extend(self.sync_paginated(url, additional_attributes))

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state



class ProjectDataSourceStream(ProjectStream):
    API_METHOD = 'GET'
    TABLE = 'project_data_source'
    KEY_PROPERTIES = ['project_id', 'dataSourceId']
    RESPONSE_RESULT_KEY = "dataSources"
    IS_SELECTED_BY_DEFAULT=True

    CACHE_RESULTS = True

    def get_url(self, project_id):
        "Return the URL to hit for data from this stream."
        base = self.get_url_base()
        path = f"/project/{project_id}/dataSources"
        return f"{base}{path}"

    def sync_data(self):
        table = self.TABLE

        project_list = self.get_all_project_ids()
        resources = list()
        for child_id in project_list:
            additional_attributes = {"project_id": child_id}
            url = self.get_url(child_id)
            LOGGER.info("Syncing data for %s %s at %s", table, child_id, url)
            resources.extend(self.sync_paginated(url, additional_attributes))

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state

