import requests
import singer
import singer.metrics
import time


LOGGER = singer.get_logger()


class ImmutaClient(requests.Session):

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config
        self.auth_token = self.get_authorization()

    def get_authorization(self):
        LOGGER.info("Retrieving authentication token.")
        auth_url = f"{self.config['immuta-host']}/bim/apikey/authenticate"
        response = requests.post(
            auth_url,
            data={"apikey": self.config["api-key"]})
        
        if response.status_code != 200:
            raise RuntimeError(response.text)
        
        return response.json().get("token")

    def make_request(self, url, method, params=None, body=None):
        LOGGER.info("Making %s request to %s (%s)", method, url, params)

        response = requests.request(
            method,
            url,
            headers={
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json",
                "user-agent": self.config["user-agent"]
            },
            params=params,
            json=body)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
