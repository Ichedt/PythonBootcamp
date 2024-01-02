"""
Day 53 - Data Entry Job Automation

tags: web scraping, beautiful soup, selenium
"""
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Clone of the Zillow website for learning purposes
URL = "https://appbrewery.github.io/Zillow-Clone"
# Browser headers from https://myhttpheader.com/
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,en-US;q=0.6",
}
FORMS_LINK = "forms link"

response = requests.get(URL, headers=HEADER, timeout=10)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# Create a list of all the links on the page using CSS Selector
all_links_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_links_elements]

# Create a list of all the addresses on the page using CSS Selector
# Remove "\n", "|" and whitespaces
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [
    address.get_text().replace(" | ", " ").strip() for address in all_address_elements
]

# Create a list of all the prices on the page using CSS Selector
# Remove unecessary text and just get the price
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [
    price.get_text().replace("/mo", "").split("+")[0]
    for price in all_price_elements
    if "$" in price.text
]

# Fill the Google Form using Selenium
# Keep the browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n, _ in enumerate(all_links):
    driver.get(FORMS_LINK)
    time.sleep(2)
    # Use XPATH to select the "short answer" field in the Google Form
    address = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    price = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    link = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    submit_button = driver.find_element(
        By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
    )
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
