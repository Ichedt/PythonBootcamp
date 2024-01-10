"""Code responsible for run the Flask server."""
import datetime as dt
import requests
from flask import Flask, render_template

app = Flask(__name__)


class Post:
    """Construct Post objects."""

    def __init__(self, post_id: int, title: str, subtitle: str, body: str) -> None:
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body


current_year = dt.datetime.today().year
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391", timeout=10).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route("/")
def home():
    """Home page."""
    return render_template(
        "index.html",
        year=current_year,
        all_posts=post_objects,
    )


@app.route("/post/<int:index>")
def post_page(index):
    """Post page."""
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template(
        "post.html",
        year=current_year,
        post=requested_post,
    )


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
