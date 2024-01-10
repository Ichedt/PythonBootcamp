"""Code responsible for run the Flask server."""
from flask import Flask, render_template
import requests

# Npoint database post
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391", timeout=10).json()

app = Flask(__name__)


@app.route("/")
def home():
    """Home page."""
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Contact page."""
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    """Post page."""
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
