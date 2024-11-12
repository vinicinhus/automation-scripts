"""
Module: chrome_driver_settings.py

This module provides a class to configure Chrome driver settings for automated web scraping.
The ChromeDriverSettings class sets up custom options for the Chrome driver to enhance automation
capabilities and manage downloads effectively. It also allows for automatic creation of the
download directory if it doesn't already exist.

Dependencies:
    - selenium.webdriver.chrome.options.Options: Options class from Selenium WebDriver for configuring Chrome driver settings.
    - pathlib.Path: For handling the creation and path management of the download directory.

Usage Example:
    from chrome_driver_settings import ChromeDriverSettings

    chrome_settings = ChromeDriverSettings(download_directory='downloads', headless_mode=True)
    options = chrome_settings.get_options()

    from selenium import webdriver
    driver = webdriver.Chrome(options=options)
"""

from typing import Optional
from selenium.webdriver.chrome.options import Options
from pathlib import Path


class ChromeDriverSettings:
    """
    A class to configure Chrome driver settings for automated web scraping.

    Attributes:
        download_directory (Optional[str]): Directory for file downloads. Created in the project root if not provided.
        headless_mode (bool): If True, enables headless mode for Chrome.
    """

    def __init__(self, download_directory: Optional[str] = None, headless_mode: bool = False):
        """
        Initialize ChromeDriverSettings with specified download directory and headless mode.

        Args:
            download_directory (Optional[str]): The directory where downloaded files will be saved.
                If None, 'downloads' directory will be created in the project root.
            headless_mode (bool): If True, enables headless mode for the browser. Default is False.
        """
        self.download_directory = download_directory or "downloads"
        self.headless_mode = headless_mode
        self._create_download_directory()

    def _create_download_directory(self) -> None:
        """Create the download directory in the project root if it does not already exist."""
        path = Path(self.download_directory)
        if not path.is_absolute():
            path = Path(__file__).parent / path  # Make path relative to project root
        path.mkdir(parents=True, exist_ok=True)

    def get_options(self) -> Options:
        """
        Get Chrome driver options with customized settings.

        Returns:
            Options: Configured Chrome driver options.
        """
        options = Options()
        if self.headless_mode:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shn-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--safebrowsing-disable-download-protection")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--log-level=3")

        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(Path(self.download_directory).resolve()),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "detach": True,
                "plugins.always_open_pdf_externally": True,
                "pdfjs.disabled": True,
            },
        )

        return options


if __name__ == "__main__":
    