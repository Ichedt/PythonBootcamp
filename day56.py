"""
Day 56 - Personal Website

tags: static files, HTML/CSS file rendering
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Return the home page."""
    return render_template("day56/index.html")


if __name__ == "__main__":
    app.run(debug=True)
