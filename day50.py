"""
Day 50 - Auto Tinder Bot

tags: this one was completed with help since I'll not be creating a Tinder account
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)

# Login with Facebook
FB_EMAIL = "email"
FB_PASSWORD = "password"
URL = "http://www.tinder.com"

# Keep the browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Click Login button
sleep(2)
login_button = driver.find_element(
    By.XPATH,
    '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button',
)
login_button.click()

# Click Login with Facebook button
sleep(2)
fb_login = driver.find_element(
    By.XPATH, '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button'
)
fb_login.click()

# Switch to Facebook window
sleep(2)
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

# Facebook login
email = driver.find_element(By.XPATH, '//*[@id="email"]')
password = driver.find_element(By.XPATH, '//*[@id="pass"]')
email.send_keys(FB_EMAIL)
password.send_keys(FB_PASSWORD)
password.send_keys(Keys.ENTER)

# Switch back to Tinder window
driver.switch_to.window(base_window)
print(driver.title)

# Allow Location
sleep(5)
allow_location_button = driver.find_element(
    By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
)
allow_location_button.click()

# Disallow Notifications
notifications_button = driver.find_element(
    By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]'
)
notifications_button.click()

# Allow Cookies
cookies_button = driver.find_element(
    By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button'
)
cookies_button.click()

# Tinder only allows 100 Likes per day, so put the code in a loop
for n in range(100):
    # Add a delay between likes
    sleep(1)
    try:
        like_button = driver.find_element(
            By.XPATH,
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button',
        )
        like_button.click()
    # Catch the cases where there's a Matched pop-up in front of the Like button
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()
        # Catch the cases where the Like button hasn't yet loaded, wait 2 seconds then try again
        except NoSuchElementException:
            sleep(2)

driver.quit()
