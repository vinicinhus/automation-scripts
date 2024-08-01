from anticaptchaofficial.recaptchav2enterpriseproxyless import *
from selenium import webdriver
from selenium.webdriver.common.by import By


class RecaptchaV2EnterpriseProxylessExample:
    def __init__(self, anticaptcha_api_key: str) -> None:
        self.anticaptcha_api_key = anticaptcha_api_key
        self.recaptcha_site_key = 'your-site-recaptcha-api-key'
        self.driver = webdriver.Chrome()
        self.solve_captcha()

    def solve_captcha(self) -> None:
        self.driver.get("https://your_site_with/recaptchav2/Enterprise/Proxyless.com")

        login_element = self.driver.find_element(By.ID, "login-id")
        login_element.send_keys("my-login")

        password_element = self.driver.find_element(By.ID, "password-id")
        password_element.send_keys("my-secret-password")

        button_element = self.driver.find_element(By.ID, "button-id")
        button_element.click()

        current_url: str = self.driver.current_url

        solver = recaptchaV2EnterpriseProxyless()
        solver.set_verbose(1)
        solver.set_key(self.anticaptcha_api_key)
        solver.set_website_url(current_url)
        solver.set_website_key(self.recaptcha_site_key)

        g_response = solver.solve_and_return_solution()

        if g_response != 0:
            self.execute_recaptcha_callback(g_response=g_response)
        else:
            raise Exception(f"Anti-Captcha finished with error: {solver.error_code}")

    def execute_recaptcha_callback(self, g_response: str):
        """JavaScript code to find the callback dynamically"""
        js_code = """
        for (let client in ___grecaptcha_cfg.clients) {
            let clientObj = ___grecaptcha_cfg.clients[client];
            for (let key in clientObj) {
                if (clientObj[key] && clientObj[key].hasOwnProperty(key)) {
                    if (clientObj[key][key].hasOwnProperty("callback")) {
                        clientObj[key][key].callback(arguments[0]);
                        return true;
                    }
                }
            }
        }
        return false;
        """

        result = self.driver.execute_script(js_code, g_response)

        if not result:
            raise Exception("Callback not found or executed.")
