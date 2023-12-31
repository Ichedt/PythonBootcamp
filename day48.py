"""
Day 48 - Automatic Cookie Clicker

tags: selenium webdriver
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "http://orteil.dashnet.org/experiments/cookie/"

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Get the cookie id
cookie = driver.find_element(By.ID, value="cookie")

# Get the upgrades ids
upgrades = driver.find_elements(By.CSS_SELECTOR, value="#store div")
upgrades_ids = [upgrade.get_attribute("id") for upgrade in upgrades]

# Set the timer for buying upgrades
timeout = time.time() + 5
five_min = time.time() + 60 * 5

while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > timeout:
        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        upgrades_prices = []

        # Convert <b> text into an integer price
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                upgrades_prices.append(cost)

        # Create a dictionary of store items and prices
        cookie_upgrades = {}
        for n, _ in enumerate(upgrades_prices):
            cookie_upgrades[upgrades_prices[n]] = upgrades_ids[n]

        # Get current cookie count
        money_element = driver.find_element(By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find the upgrades that can be bought
        buyable_upgrades = {}
        for cost, identifier in cookie_upgrades.items():
            if cookie_count > cost:
                buyable_upgrades[cost] = identifier

        # Purchase the most expensive buyable upgrade
        highest_price_buyable_upgrade = max(buyable_upgrades)
        to_purchase_id = buyable_upgrades[highest_price_buyable_upgrade]
        driver.find_element(By.ID, value=to_purchase_id).click()

        # Add 5 seconds until the next check
        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID, value="cps").text
        print(cookie_per_sec)
        break

# Close a single tab
# driver.close()

# Close the whole window
driver.quit()
