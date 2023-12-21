"""
Day 36 - Stock News Monitoring Project

tags: 
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

alphavantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHAVANTAGE_API_KEY,
}

# 1. Get yesterday's closing stock price
stock_response = requests.get(STOCK_ENDPOINT, params=alphavantage_params, timeout=10)
stock_data = stock_response.json()["Time Series (Daily)"]
# Transform the dates in list indexes
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# 2. Get the day before yesterday's closing stock price
day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# 3. Find the positive difference between 1 and 2
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"


# 4. Find the percentage difference in price between both closing prices
difference_percent = round((difference / float(yesterday_closing_price)) * 100)

# 5. If the percentage is greater than 5, get the first 3 news pieces for the COMPANY_NAME
if abs(difference_percent) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params, timeout=10)
    articles = news_response.json()["articles"]
    # 6. Create a list with the first 3 articles
    three_articles = articles[:3]
    # 7. Format the articles
    formatted_articles = [
        f"""{STOCK_NAME} {up_down} {difference_percent}%
Headline: {article["title"]}.
Brief: {article["description"]}"""
        for article in three_articles
    ]
    print(formatted_articles)
