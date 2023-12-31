"""
Day 45 - Top 100 Movies using Web Scraping

tags: web scraping, beautiful soup
"""
from bs4 import BeautifulSoup
import requests

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL, timeout=10)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_movies = soup.find_all(name="h3", class_="title")
movie_titles = [movie.getText() for movie in all_movies]
# Reverse the order of the list
movies = movie_titles[::-1]

# Create a text file with the list of the movies
with open("movies.txt", mode="w", encoding="utf-8") as file:
    for movie in movies:
        file.write(f"{movie}\n")
