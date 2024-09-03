from bitrix24_api import Bitrix24API

bitrix_api = Bitrix24API(webhook_url="https://your-webhook-url.com")

post_response = bitrix_api.send_post_request("tasks.task.add", {"fields": {"TITLE": "New Task"}})

get_response = bitrix_api.send_get_request("tasks.task.get", {"taskId": 123})
