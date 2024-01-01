"""
Day 51 - Complaining Twitter Bot

tags:
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

MIN_DOWNLOAD_SPEED = 150
MIN_UPLOAD_SPEED = 10
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
TWITTER_EMAIL = "email"
TWITTER_PASSWORD = "password"


class InternetSpeedTwitterBot:
    """Manage the bot and its functionalities."""

    def __init__(self, driver_path):
        """Initialize the required attributes."""
        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        """Go to the SpeedTest website and get the internet speed."""
        self.driver.get("https://www.speedtest.net/")

        time.sleep(3)
        go_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-button a")
        go_button.click()
        time.sleep(60)
        self.up = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span',
        ).text
        self.down = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span',
        ).text

    def tweet_at_provider(self):
        """Go to Twitter and make a tweet complaining about the internet speed."""
        self.driver.get("https://twitter.com/login")

        time.sleep(2)
        email = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input',
        )
        password = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input',
        )
        email.send_keys(TWITTER_EMAIL)
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        tweet_compose = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div',
        )
        tweet = f"Hey @InternetProvider, why is mt internet speed {self.down}down/{self.up}up when I pay for {MIN_DOWNLOAD_SPEED}down/{MIN_UPLOAD_SPEED}up?"
        tweet_compose.send_keys(tweet)
        time.sleep(3)
        tweet_button = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]',
        )
        tweet_button.click()
        time.sleep(2)
        self.driver.quit()


def main():
    """Run the main code."""
    bot = InternetSpeedTwitterBot(CHROME_PATH)
    bot.get_internet_speed()
    bot.tweet_at_provider()


if __name__ == "__main__":
    main()
