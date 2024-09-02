from bot_configuration import Bot, DriverType


def main():
    # Initialize the Bot object with anti-captcha key, headless mode, and Chrome driver
    bot = Bot(
        anticaptcha_key="your_anticaptcha_key",  # Replace with your actual anti-captcha key
        headless_mode=True,  # Run browser in headless mode
        driver=DriverType.CHROME,  # Use Chrome browser
    )

    # The bot will start the browser with the specified configuration
    print("Browser started with the following configuration:")
    print(f"Driver Path: {bot._bot.driver_path}")
    print(f"Headless Mode: {bot._bot.headless}")
    print(f"Browser: {bot._bot.browser.name}")

    # Your automation tasks go here
    # e.g., bot.start_browser()
    #       bot.browse("https://www.google.com/")
    #       bot.stop_browser()


if __name__ == "__main__":
    main()
