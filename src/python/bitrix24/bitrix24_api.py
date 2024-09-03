import requests
from typing import Dict, Any

class Bitrix24API:
    """
    A class to interact with the Bitrix24 API using a provided webhook.
    """

    def __init__(self, webhook_url: str) -> None:
        """
        Initializes the Bitrix24API instance with the provided webhook URL.
        
        :param webhook_url: The base URL of the Bitrix24 webhook.
        """
        self.webhook_url = webhook_url

    def send_post_request(self, method: str, params: Dict[str, Any]) -> requests.Response:
        """
        Sends a POST request to the Bitrix24 API.

        :param method: The API method to be called (e.g., 'tasks.task.add').
        :param params: The parameters to be sent in the request body.
        :return: The response object from the requests library.
        """
        url = f"{self.webhook_url}/{method}"
        response = requests.post(url, json=params)
        response.raise_for_status()
        return response

    def send_get_request(self, method: str, params: Dict[str, Any]) -> requests.Response:
        """
        Sends a GET request to the Bitrix24 API.

        :param method: The API method to be called (e.g., 'tasks.task.get').
        :param params: The parameters to be sent as query string.
        :return: The response object from the requests library.
        """
        url = f"{self.webhook_url}/{method}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
