const TelegramManager = require('./telegram_manager');

(async () => {
    // Initialize a TelegramManager object with your bot token and chat ID
    const token = 'YOUR_TELEGRAM_BOT_TOKEN';
    const chatId = 'YOUR_CHAT_ID';
    const manager = new TelegramManager(token, chatId);

    // Send a message to the Telegram group
    const message = 'Hello, Telegram Group!';
    try {
        const response = await manager.sendMessageToGroup(message);
        console.log('Message sent successfully:', response);
    } catch (error) {
        console.error('Error sending message:', error);
    }

    // Stop the bot from polling (optional, if you need to stop the bot)
    manager.stopBot();
})();