"""
Module: bitrix24_api

This module provides the `Bitrix24API` class for interacting with the Bitrix24 API using a provided webhook URL.

The class allows for sending POST and GET requests to the Bitrix24 API, enabling interaction with various API methods.

Dependencies:
    requests: A library for making HTTP requests, which supports sending GET and POST requests and handling responses.

Classes:
    Bitrix24API: A class that interacts with the Bitrix24 API by sending POST and GET requests. It requires a webhook URL for initialization and provides methods for making API calls.

Usage Example:
    >>> from bitrix24_api import Bitrix24API

    >>> # Initialize a Bitrix24API object with a webhook URL
    >>> bitrix_api = Bitrix24API(webhook_url="https://your-webhook-url.com")

    >>> # Send a POST request to add a new task
    >>> post_response = bitrix_api.send_post_request("tasks.task.add", {"fields": {"TITLE": "New Task"}})

    >>> # Send a GET request to retrieve a task by its ID
    >>> get_response = bitrix_api.send_get_request("tasks.task.get", {"taskId": 123})

    >>> # Both responses will be of type requests.Response
"""

from typing import Dict, Any

import requests


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

    def send_post_request(
        self, method: str, params: Dict[str, Any]
    ) -> requests.Response:
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

    def send_get_request(
        self, method: str, params: Dict[str, Any]
    ) -> requests.Response:
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
