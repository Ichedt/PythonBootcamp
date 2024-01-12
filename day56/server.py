"""Code responsible for running the Flask server."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
