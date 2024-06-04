/**
 * Module: puppeteerHelper.js
 * 
 * This module provides a helper class to interact with web elements using Puppeteer.
 * It encapsulates common Puppeteer operations into methods for ease of use and better maintainability.
 * 
 * Dependencies:
 *    - puppeteer: A Node.js library which provides a high-level API to control Chrome or Chromium over the DevTools Protocol.
 * 
 * Usage Example:
 *    const puppeteer = require('puppeteer');
 *    const PuppeteerHelper = require('./puppeteer_helper');
 * 
 *    (async () => {
 *        const browser = await puppeteer.launch();
 *        const page = await browser.newPage();
 *        const puppeteerHelper = new PuppeteerHelper(page);
 * 
 *        await page.goto('https://example.com');
 * 
 *        // Example usage
 *        await puppeteerHelper.clickElement('button#submit');
 *        await puppeteerHelper.typeIntoElement('input#username', 'example_user');
 * 
 *        await browser.close();
 *    })();
 */

const puppeteer = require('puppeteer');

class PuppeteerHelper {
    /**
     * Constructor for PuppeteerHelper.
     * 
     * @param {Page} page - The Puppeteer Page instance to interact with.
     */
    constructor(page) {
        this.page = page;
    }

    /**
     * Type text into a visible element identified by a CSS selector.
     * 
     * @param {string} selector - The CSS selector of the element.
     * @param {string} text - The text to be typed into the element.
     * @param {number} [timeout=10000] - Maximum time to wait for the element in milliseconds. Defaults to 10 seconds.
     */
    async typeIntoElement(selector, text, timeout = 10000) {
        await this.page.waitForSelector(selector, { visible: true, timeout });
        await this.page.type(selector, text);
    }

    /**
     * Click a visible element identified by a CSS selector.
     * 
     * @param {string} selector - The CSS selector of the element.
     * @param {number} [timeout=10000] - Maximum time to wait for the element to be clickable in milliseconds. Defaults to 10 seconds.
     */
    async clickElement(selector, timeout = 10000) {
        await this.page.waitForSelector(selector, { visible: true, timeout });
        await this.page.click(selector);
    }

    /**
     * Clear the text of a visible element identified by a CSS selector.
     * 
     * @param {string} selector - The CSS selector of the element.
     * @param {number} [timeout=10000] - Maximum time to wait for the element in milliseconds. Defaults to 10 seconds.
     */
    async clearElementText(selector, timeout = 10000) {
        await this.page.waitForSelector(selector, { visible: true, timeout });
        await this.page.$eval(selector, element => element.value = '');
    }

    /**
     * Select an option from a dropdown element by its value attribute.
     * 
     * @param {string} selector - The CSS selector of the dropdown element.
     * @param {string} optionValue - The value attribute of the option to be selected.
     * @param {number} [timeout=10000] - Maximum time to wait for the element in milliseconds. Defaults to 10 seconds.
     */
    async selectDropdownOptionByValue(selector, optionValue, timeout = 10000) {
        await this.page.waitForSelector(selector, { visible: true, timeout });
        await this.page.select(selector, optionValue);
    }

    /**
     * Switch to an iframe identified by a CSS selector.
     * 
     * @param {string} selector - The CSS selector of the iframe.
     * @returns {Frame} - The Puppeteer Frame instance of the iframe.
     */
    async switchToIframe(selector) {
        const iframeElement = await this.page.waitForSelector(selector);
        const iframe = await iframeElement.contentFrame();
        await this.page.waitFor(1000); // Wait for a brief moment for the iframe to fully load
        await this.page.evaluate(() => document.activeElement.blur()); // Blur the active element
        await this.page.waitFor(1000); // Wait for a brief moment after blurring active element
        return iframe;
    }

    /**
     * Check if an element identified by a CSS selector is present on the web page.
     * 
     * @param {string} selector - The CSS selector of the element.
     * @returns {boolean} - True if the element is present, False otherwise.
     */
    async isElementPresent(selector) {
        return await this.page.$(selector) !== null;
    }
}

module.exports = PuppeteerHelper;
