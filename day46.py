"""
Day 46 - Musical Time Machine

tags: beautiful soup, web scraping
"""
from bs4 import BeautifulSoup
import requests

date_choice = input("Which year do you want to travel to? [YYYY-MM-DD]: ")

response = requests.get(
    f"https://www.billboard.com/charts/hot-100/{date_choice}",
    timeout=10,
)

soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
