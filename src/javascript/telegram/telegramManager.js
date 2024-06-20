/**
 * Module: telegramManager.js
 *
 * This module provides a class for sending messages to a Telegram group using the node-telegram-bot-api library.
 *
 * Classes:
 *     TelegramManager: A class for managing a Telegram bot to send messages to a group.
 *
 * Dependencies:
 *     node-telegram-bot-api: A library for interacting with the Telegram Bot API.
 *
 * Usage Example:
 *     const TelegramManager = require('./telegram_manager');
 *
 *     // Initialize a TelegramManager object
 *     const token = 'YOUR_TELEGRAM_BOT_TOKEN';
 *     const chatId = 'YOUR_CHAT_ID';
 *     const manager = new TelegramManager(token, chatId);
 *
 *     // Send a message to the group
 *     const message = 'Hello, Telegram Group!';
 *     manager.sendMessageToGroup(message)
 *         .then(response => console.log('Message sent successfully:', response))
 *         .catch(error => console.error('Error sending message:', error));
 */

const TelegramBot = require("node-telegram-bot-api");

class TelegramManager {
  /**
   * Initializes the TelegramManager with the provided token and chat ID.
   *
   * @param {string} token - The token of the Telegram bot.
   * @param {string} chatId - The chat ID of the Telegram group.
   */
  constructor(token, chatId) {
    this.bot = new TelegramBot(token, { polling: true });
    this.chatId = chatId;
  }

  /**
   * Sends a message to the Telegram group.
   *
   * @param {string} message - The message to be sent to the group.
   * @returns {Promise<Object>} - The response from the Telegram API.
   * @throws {Error} - If there is an error sending the message.
   */
  async sendMessageToGroup(message) {
    try {
      const response = await this.bot.sendMessage(this.chatId, message);
      console.log("Message sent successfully:", response);
      return response;
    } catch (error) {
      console.error("Error sending message:", error);
      throw error;
    }
  }

  /**
   * Stops the Telegram bot from polling for new messages.
   */
  stopBot() {
    this.bot.stopPolling();
    console.log("TelegramSender Bot stopped.");
  }
}

module.exports = TelegramManager;
