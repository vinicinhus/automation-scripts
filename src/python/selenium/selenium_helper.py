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

from typing import Literal, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait


class SeleniumHelper:
    """
    A helper class to interact with web elements using Selenium WebDriver.

    Args:
        driver (webdriver.Chrome): An instance of Selenium WebDriver.
    """

    DEFAULT_TIMEOUT: int = 10

    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Initialize SeleniumHelper with a WebDriver instance.

        Args:
            driver (webdriver): An instance of Selenium WebDriver.
        """
        self.driver = driver

    def _locator(self, by: Union[By, str], locator: str) -> tuple[str, str]:
        """
        Internal helper to normalize locator typing for Selenium expected_conditions.
        Ensures compatibility between By enums and plain strings.

        Args:
            by (Union[By, str]): The Selenium locator type (e.g., By.ID, "id").
            locator (str): The locator value.

        Returns:
            tuple[str, str]: A properly typed locator tuple for Selenium conditions.
        """
        return (str(by), locator)

    def type_into_element(
        self,
        by: Union[By, str],
        locator: str,
        text: str,
        timeout: int = DEFAULT_TIMEOUT,
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
        element = wait.until(
            ec.visibility_of_element_located(self._locator(by, locator))
        )
        element.send_keys(text)

    def click_element(
        self, by: Union[By, str], locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Click a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element to be clickable in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(ec.element_to_be_clickable(self._locator(by, locator)))
        element.click()

    def clear_element_text(
        self, by: Union[By, str], locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Clear the text of a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(
            ec.visibility_of_element_located(self._locator(by, locator))
        )
        element.clear()

    def select_dropdown_option_by_value(
        self,
        by: Union[By, str],
        locator: str,
        option_value: str,
        timeout: int = DEFAULT_TIMEOUT,
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
        element = wait.until(ec.presence_of_element_located(self._locator(by, locator)))
        select = Select(element)
        select.select_by_value(option_value)

    def switch_to_iframe(self, by: Union[By, str], locator: str) -> None:
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
        iframe = wait.until(ec.presence_of_element_located(self._locator(by, locator)))
        self.driver.switch_to.frame(iframe)

    def is_element_present(
        self,
        by: Union[By, str],
        locator: str,
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
            self.driver.find_element(str(by), locator)
            return True
        except NoSuchElementException:
            return False

    def get_element_text(
        self, by: Union[By, str], locator: str, timeout: int = DEFAULT_TIMEOUT
    ) -> str:
        """
        Retrieve the text content of a visible element identified by a locator.

        Args:
            by (By): The locator strategy (e.g., By.ID, By.XPATH, By.NAME, etc.).
            locator (str): The value of the locator for the element.
            timeout (int): Maximum time to wait for the element in seconds. Defaults to 10 seconds.

        Returns:
            str: The text content of the element. If the element is not found, returns an empty string.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(
                ec.visibility_of_element_located(self._locator(by, locator))
            )
            return element.text
        except NoSuchElementException:
            return ""

    def handle_alert(
        self, action: Literal["a", "d"] = "a", timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Handle browser alerts (JavaScript pop-ups) by accepting or dismissing them.

        This function waits for a browser alert to be present within the given timeout period.
        Once detected, it performs the specified action — either accepting ('a') or dismissing ('d') the alert.

        Args:
            action (str): Action to perform on the alert.
                          Use 'a' for accept (default) or 'd' for dismiss.
            timeout (int): Maximum time to wait for the alert in seconds. Defaults to 10 seconds.

        Raises:
            TimeoutException: If the alert does not appear within the specified timeout.
            UnexpectedAlertPresentException: If an unexpected alert is already open.
            ValueError: If the action value is not 'a' or 'd'.
        """
        wait = WebDriverWait(self.driver, timeout)
        alert = wait.until(lambda d: d.switch_to.alert)

        if action.lower() == "a":
            alert.accept()
        elif action.lower() == "d":
            alert.dismiss()
        else:
            raise ValueError("Invalid action. Use 'a' for accept or 'd' for dismiss.")
