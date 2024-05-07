import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.python.selenium.selenium_helper import SeleniumHelper


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def helper(driver):
    url = "http://example.com/"
    driver.get(url)
    return SeleniumHelper(driver)


def test_wait_for_element_presence(helper):
    element = helper.wait_for_element_presence(By.ID, "element_id")
    assert element is not None


def test_type_into_element(helper):
    helper.type_into_element(By.ID, "element_id", "text")
    element = helper.driver.find_element(By.ID, "element_id")
    assert element.get_attribute("value") == "text"


def test_click_element(helper):
    helper.click_element(By.ID, "element_id")
    # You can add assertions here based on the expected behavior after clicking


def test_clear_element_text(helper):
    helper.clear_element_text(By.ID, "element_id")
    element = helper.driver.find_element(By.ID, "element_id")
    assert element.get_attribute("value") == ""


def test_select_dropdown_option_by_value(helper):
    helper.select_dropdown_option_by_value(By.ID, "dropdown_id", "option_value")
    # You can add assertions here based on the expected behavior after selecting the option


def test_is_element_present(helper):
    assert helper.is_element_present(By.ID, "element_id")
