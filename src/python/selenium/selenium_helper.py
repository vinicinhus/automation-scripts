"""
Module: selenium_helper.py

This module provides a helper class to interact with web elements using Selenium WebDriver.
It encapsulates common Selenium operations into methods for ease of use and better maintainability.

Dependencies:
    - selenium: A powerful tool for controlling web browsers through programs and performing browser automation.

Usage Example::
    from selenium import webdriver
    from selenium_helper import SeleniumHelper
    
    driver = webdriver.Chrome()
    
    helper = SeleniumHelper(driver)
    
    helper.click_element(By.ID, "button_id")
"""

from typing import Union

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

    def wait_for_element_presence(
            self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Union[webdriver.remote.webelement.WebElement, None]:
        """
        Wait for an element to be present on the web page.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.) for the element.
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.

        Returns:
            WebElement: The located element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(ec.presence_of_element_located((by, locator)))

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
        element = self.wait_for_element_presence(by, locator, timeout)
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
        element = self.wait_for_element_presence(by, locator, timeout)
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
        element = self.wait_for_element_presence(by, locator, timeout)
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
        element = self.wait_for_element_presence(by, locator, timeout)
        select = Select(element)
        select.select_by_value(option_value)

    def is_element_present(
            self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """
        Check if an element identified by a locator is present on the web page.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.) for the element.
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            self.wait_for_element_presence(by, locator, timeout)
            return True
        except NoSuchElementException:
            return False
