"""
Module: selenium_helper.py

This module provides a helper class to interact with web elements using Selenium WebDriver.
It encapsulates common Selenium operations into methods for ease of use and better maintainability.

Dependencies:
    - selenium: A powerful tool for controlling web browsers through programs and performing browser automation.

Usage Example::
    >>> from selenium import webdriver
    >>> from selenium_helper import SeleniumHelper
    
    >>> driver = webdriver.Chrome()
    >>> helper = SeleniumHelper(driver)
    >>> helper.click_element(By.ID, "button_id")
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait, Select

DEFAULT_TIMEOUT: int = 10


class SeleniumHelper:
    """
    A helper class to interact with web elements using Selenium WebDriver.

    Args:
        driver (webdriver.Chrome): An instance of Selenium WebDriver.
    """

    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Initialize SeleniumHelper with a WebDriver instance.

        Args:
            driver (webdriver): An instance of Selenium WebDriver.
        """
        self.driver = driver

    def type_into_element(
            self, by: By, locator: str, text: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Type text into a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            text (str): The text to be typed into the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(ec.visibility_of_element_located((by, locator)))
        element.send_keys(text)

    def click_element(
            self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Click a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element to be clickable in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(ec.element_to_be_clickable((by, locator)))
        element.click()

    def clear_element_text(
            self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Clear the text of a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(ec.visibility_of_element_located((by, locator)))
        element.clear()

    def select_dropdown_option_by_value(
            self, by: By, locator: str, option_value: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Select an option from a dropdown element by its value attribute.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            option_value (str): The value attribute of the option to be selected.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(ec.visibility_of_element_located((By, locator)))
        select = Select(element)
        select.select_by_value(option_value)

    def switch_to_iframe(self, by: By, locator: str) -> None:
        """
        Switch to an iframe identified by a locator.

        This function waits for the iframe to be present on the web page and then switches the driver's context to the
        iframe.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.) for the iframe.
            locator (str): The value of the locator for the iframe.

        Returns:
            None
        """
        wait = WebDriverWait(self.driver, 30)
        iframe = wait.until(ec.presence_of_element_located((by, locator)))
        self.driver.switch_to.frame(iframe)

    def is_element_present(
            self, by: By, locator: str,
    ) -> bool:
        """
        Check if an element identified by a locator is present on the web page.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.) for the element.
            locator (str): The value of the locator for the element.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False
