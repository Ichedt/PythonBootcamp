"""
Day 52 - Instagram Follower Bot

tags: selenium webdriver
"""
import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

SIMILAR_ACCOUNT = "account"
USERNAME = "email"
PASSWORD = "password"
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"


class InstaFollower:
    """Manage the following bot."""

    def __init__(self, driver_path: str) -> None:
        """Initialize the driver."""
        # Keep the browser open
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options,
        )

    def login(self) -> None:
        """Login into Instagram."""
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(4)
        # In case the Cookies warning appear
        decline_cookies_xpath = (
            "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        )
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            # Dismiss by clicking the button
            cookie_warning[0].click()
        # Login
        username = self.driver.find_element(By.NAME, value="username")
        password = self.driver.find_element(By.NAME, value="password")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        time.sleep(3)
        password.send_keys(Keys.ENTER)
        # Click "Not now" in Save Login prompt
        time.sleep(4)
        save_login_prompt = self.driver.find_element(
            By.XPATH, value="//div[contains(text(), 'Not now')]"
        )
        if save_login_prompt:
            save_login_prompt.click()
        # Click "Not now" in Notifications prompt
        time.sleep(3)
        notifications_prompt = self.driver.find_element(
            By.XPATH, value="// button[contains(text(), 'Not Now')]"
        )
        if notifications_prompt:
            notifications_prompt.click()

    def find_followers(self) -> None:
        """Navigate to the followers window."""
        time.sleep(5)
        # Show followers for the selected account
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")
        time.sleep(5)
        modal_xpath = (
            "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        )
        modal = self.driver.find_element(By.XPATH, value=modal_xpath)
        for i in range(10):
            # Scroll to the top of the modal element by its height using JavaScript
            # so each time you follow, the next account is at the top of the modal
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", modal
            )
            time.sleep(2)

    def follow(self) -> None:
        """Follow each account."""
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, value="._aano button")
        for button in all_buttons:
            try:
                button.click()
                time.sleep(2)
            # If you already follow the account, it will trigger a dialog to unfollow/cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(
                    By.XPATH, value="//button[contains(text(), 'Cancel')]"
                )
                cancel_button.click()


def main() -> None:
    """Run the main code."""
    bot = InstaFollower(CHROME_PATH)
    bot.login()
    bot.find_followers()
    bot.follow()


if __name__ == "__main__":
    main()
