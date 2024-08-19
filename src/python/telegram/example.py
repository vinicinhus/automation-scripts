import asyncio

from telegram_manager import TelegramManager


async def main():
    # Replace these with your actual bot token and chat ID
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"

    # Initialize the TelegramManager
    manager = TelegramManager(token=token, chat_id=chat_id)

    # Message to be sent
    message = "Hello, Telegram Group!"

    # Send the message
    await manager.send_message_to_group(message)


if __name__ == "__main__":
    asyncio.run(main())
