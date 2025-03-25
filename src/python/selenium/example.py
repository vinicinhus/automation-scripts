from chrome_driver_settings import ChromeDriverSettings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_helper import SeleniumHelper


def main():
    # Initialize ChromeDriver with custom settings
    chrome_settings = ChromeDriverSettings(
        download_directory="downloads", headless_mode=True, incognito_mode=True
    )
    options = chrome_settings.get_options()
    print("ChromeDriver initialized with custom settings.")

    driver = webdriver.Chrome(options=options)

    # Initialize SeleniumHelper with the WebDriver instance
    helper = SeleniumHelper(driver)

    try:
        # Open a webpage
        driver.get("https://www.example.com")

        # Interact with elements on the page
        helper.click_element(By.ID, "start-button")
        input()
        helper.type_into_element(By.NAME, "username", "test_user")
        helper.type_into_element(By.NAME, "password", "test_password")
        helper.click_element(By.XPATH, "//button[@type='submit']")

        # Check if an element is present
        if helper.is_element_present(By.CLASS_NAME, "welcome-message"):
            welcome_text = helper.get_element_text(By.CLASS_NAME, "welcome-message")
            print(f"Login successful: {welcome_text}")
        else:
            print("Login failed: Welcome message not found.")

        # Select an option from a dropdown menu
        helper.select_dropdown_option_by_value(By.ID, "dropdown-menu", "option_value")

        # Switch to an iframe and interact with elements inside it
        helper.switch_to_iframe(By.TAG_NAME, "iframe")
        helper.click_element(By.XPATH, "//button[@class='inside-iframe-button']")

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    main()
