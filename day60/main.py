"""Code responsible for running the Flask server."""
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def log_in():
    """Login page. Receive the data from the form."""
    username = request.form["username"]
    password = request.form["password"]
    return render_template("login.html", username=username, passcode=password)


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
