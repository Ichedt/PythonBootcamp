"""
Day 47 - Amazon Price Tracker

tags: beautiful soup, web scraping
"""
from bs4 import BeautifulSoup
import requests
import lxml

PRODUCT_URL = "https://www.amazon.com.br/kindle-11geracao-preto/dp/B09SWTG9GF/?_encoding=UTF8&pd_rd_w=FbGJ0&content-id=amzn1.sym.52e74d21-088e-4a9d-888d-8b14bf95d4ae&pf_rd_p=52e74d21-088e-4a9d-888d-8b14bf95d4ae&pf_rd_r=Z0X575WW5094W4J2VDJ3&pd_rd_wg=e69AK&pd_rd_r=59df36f9-19e0-4e42-8067-12e25ef4bee7&ref_=pd_gw_crs_zg_bs_16333486011&th=1"
# Headers necessary to get the webpage, available at: https://myhttpheader.com
headers = {
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
}

# Get the response and soup it using lxml
response = requests.get(url=PRODUCT_URL, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price_whole = soup.find(class_="a-price-whole").get_text()
price_decimal = soup.find(class_="a-price-fraction").get_text()
price = float(f"{price_whole.replace(',','')}.{price_decimal}")
print(price)

# The email part isn't really necessary so I'll be avoiding using my email for
# coding.
