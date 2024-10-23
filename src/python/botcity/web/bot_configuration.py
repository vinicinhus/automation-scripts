"""
Module: bot_configuration

This module provides the `Bot` class for configuring and initializing a web automation bot using BotCity's WebBot.

The class allows for setting up the browser with various options based on the chosen driver (Chrome, Firefox, or Edge) and configuring the bot's behavior such as running in headless mode.

Dependencies:
    botcity-framework-web: A library for web automation, including support for various web browsers and tools for solving CAPTCHAs.
    enum: A module that provides support for creating enumerations, which are a set of symbolic names bound to unique, constant integer values.

Classes:
    Bot: A class that initializes a web automation bot with anti-captcha credentials and browser configuration. It sets up the browser based on the selected driver and desired options.

Usage Example:
    >>> from bot_configuration import Bot, DriverType

    >>> # Initialize a Bot object with anti-captcha key, headless mode, and Chrome driver
    >>> bot = Bot(
    ...     anticaptcha_key='your_anticaptcha_key',
    ...     headless_mode=True,
    ...     driver=DriverType.CHROME
    ... )

    >>> # The bot will start the browser with the specified configuration
    >>> # The browser will be in headless mode with the specified driver
"""

from enum import Enum
from typing import Optional

from botcity.web import WebBot, Browser, PageLoadStrategy
from botcity.web.browsers.chrome import default_options as default_options_chrome
from botcity.web.browsers.edge import default_options as default_options_edge
from botcity.web.browsers.firefox import default_options as default_options_firefox


class DriverType(Enum):
    CHROME = "CHROME"
    FIREFOX = "FIREFOX"
    EDGE = "EDGE"


class Bot:
    def __init__(
        self,
        anticaptcha_key: Optional[str],
        headless_mode: bool,
        driver: DriverType,
    ) -> None:
        """
        Initialize the Bot with anticaptcha credentials and browser configuration.

        :param anticaptcha_key: The anti-captcha key for solving CAPTCHAs. Can be None or a string.
        :param headless_mode: Whether to run the browser in headless mode.
        :param driver: The browser driver to use (CHROME, FIREFOX, or EDGE).
        """
        self._anticaptcha_key = anticaptcha_key
        self._headless_mode = headless_mode
        self._driver = driver

        self._bot = WebBot()
        self._setup_browser()

    def _setup_browser(self) -> None:
        """
        Set up the browser with the appropriate settings based on the chosen driver.
        """
        self._bot.headless = self._headless_mode
        self._bot.download_folder_path = "downloads"

        if self._driver == DriverType.CHROME:
            self._bot.driver_path = r"tools\drivers\chromedriver.exe"
            self._bot.browser = Browser.CHROME
            default_options = default_options_chrome(
                headless=self._bot.headless,
                download_folder_path=self._bot.download_folder_path,
                user_data_dir=None,
                page_load_strategy=PageLoadStrategy.NORMAL,
            )
            default_options.binary_location = (
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )
        elif self._driver == DriverType.FIREFOX:
            self._bot.driver_path = r"tools\drivers\geckodriver.exe"
            self._bot.browser = Browser.FIREFOX
            default_options = default_options_firefox(
                headless=self._bot.headless,
                download_folder_path=self._bot.download_folder_path,
                user_data_dir=None,
                page_load_strategy=PageLoadStrategy.NORMAL,
            )
            default_options.binary_location = (
                r"C:\Program Files\Mozilla Firefox\firefox.exe"
            )
        elif self._driver == DriverType.EDGE:
            self._bot.driver_path = r"tools\drivers\msedgedriver.exe"
            self._bot.browser = Browser.EDGE
            default_options = default_options_edge(
                headless=self._bot.headless,
                download_folder_path=self._bot.download_folder_path,
                user_data_dir=None,
                page_load_strategy=PageLoadStrategy.NORMAL,
            )
            default_options.binary_location = (
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            )

        self._bot.options = default_options
        self._bot.start_browser()
