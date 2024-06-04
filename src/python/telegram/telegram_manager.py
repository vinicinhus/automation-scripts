"""
Module: telegram_manager.py

This module provides a class for sending messages to a Telegram group using the python-telegram-bot library and logging with Loguru.

Classes:
    TelegramManager: A class for managing a Telegram bot to send messages to a group.

Dependencies:
    python-telegram-bot: A wrapper for the Telegram Bot API.
    loguru: A library for logging in Python with simplicity and power.

Usage Example:
    >>> from telegram_manager import TelegramManager
    >>> import asyncio

    >>> # Initialize a TelegramManager object
    >>> token = 'YOUR_TELEGRAM_BOT_TOKEN'
    >>> chat_id = 'YOUR_CHAT_ID'
    >>> manager = TelegramManager(token, chat_id)

    >>> # Send a message to the group
    >>> message = 'Hello, Telegram Group!'
    >>> asyncio.run(manager.send_message_to_group(message))
"""

from telegram import Bot
from telegram.error import TelegramError
from loguru import logger


class TelegramManager:
    """
    A class for managing a Telegram bot to send messages to a group.
    """
    def __init__(self, token: str, chat_id: str) -> None:
        """
        Initializes the TelegramManager with the provided token and chat ID.

        Args:
            token (str): The token of the Telegram bot.
            chat_id (str): The chat ID of the Telegram group.
        """
        self.token = token
        self.chat_id = chat_id
        self.bot = Bot(token=self.token)

        logger.add("file.log", rotation="1 MB")

    async def send_message_to_group(self, message: str) -> None:
        """
        Sends a message to the Telegram group.

        Args:
            message (str): The message to be sent to the group.

        Raises:
            TelegramError: If there is an error sending the message.
        """
        try:
            logger.info(f"Sending message to chat_id {self.chat_id}")
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            logger.info(f"Message sent: {message}")
        except TelegramError as e:
            logger.error(f"Failed to send message: {e}")
