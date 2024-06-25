"""
Module: chrome_driver_settings.py

This module provides a function to configure Chrome driver settings for automated web scraping.
It sets up custom options for the Chrome driver to enhance automation capabilities and manage downloads effectively.

Dependencies:
    - selenium.webdriver.chrome.options.Options: Options class from Selenium WebDriver for configuring Chrome driver settings.

Usage Example:
    from selenium import webdriver
    from chrome_driver_settings import driver_settings
    
    driver = webdriver.Chrome()
    
    options = driver_settings(download_directory='/path/to/download/directory', headless_mode=True)
    driver = webdriver.Chrome(chrome_options=options)
"""

from typing import Optional

from selenium.webdriver.chrome.options import Options


def driver_settings(download_directory: Optional[str] = None, headless_mode: bool = False) -> Options:
    """
    Configure Chrome driver settings for automated web scraping.

    Args:
        download_directory (Optional[str]): The directory where downloaded files will be saved.
        headless_mode (bool): If True, enables headless mode for the browser. Default is False.

    Returns:
        selenium.webdriver.chrome.options.Options: Chrome driver options with custom settings.
    """
    options = Options()
    if headless_mode:
        options.add_argument("--headless=new") # Enables headless mode for the browser
    options.add_argument("--disable-gpu")  # Disable GPU for the browser
    options.add_argument("--disable-dev-shn-usage")  # Disable developer usage features
    options.add_argument("--start-maximized")  # Start the browser in maximized fullscreen mode
    options.add_argument(
        "--safebrowsing-disable-download-protection")  # Disable download protection provided by Safe Browsing
    options.add_argument("--disable-extensions")  # Disables Chrome extensions.
    options.add_argument(
        "--ignore-certificate-errors")  # Ignores SSL certificate errors, allowing Chrome to load pages with HTTPS errors.
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-infobars")  # Disable the 'infobars' that pop up at the top of Chrome windows.
    options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
    options.add_argument('--log-level=3')

    if download_directory:
        options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "detach": True,
            "plugins.always_open_pdf_externally": True,
            "pdfjs.disabled": True
        })

    return options
