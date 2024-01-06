"""
Day 57 - Blog Website;

tags: url building, jinja, flask
"""
import datetime as dt
from flask import Flask, render_template
import requests

app = Flask(__name__)


class Post:
    """Class responsible for constructing a Post instance."""

    def __init__(self, post_id: int, title: str, subtitle: str, body: str):
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body


# Getting the posts
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391", timeout=10).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route("/")
def get_all_posts():
    """Homepage of the website."""
    current_year = dt.datetime.now().year
    return render_template(
        "day57/index.html",
        year=current_year,
        all_posts=post_objects,
    )


@app.route("/post/<int:index>")
def show_post(index):
    """Show selected post."""
    current_year = dt.datetime.now().year
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template(
        "day57/post.html",
        year=current_year,
        post=requested_post,
    )


if __name__ == "__main__":
    app.run(debug=True)
