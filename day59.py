"""
Day 59 - Blog Website (Improved)

tags: flask, web development
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Home page."""
    return render_template("day59/index.html")


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
