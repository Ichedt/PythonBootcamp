"""Code responsible for running the Flask server."""
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5


class LoginForm(FlaskForm):
    """Class responsible for generating the form fields."""

    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")


app = Flask(__name__)


@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if (
            login_form.email.data == "admin@email.com"
            and login_form.password.data == "123456"
        ):
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)


def main() -> None:
    """Run the main code."""
    app.secret_key = "abba1221"
    Bootstrap5(app)
    app.run(debug=True)


if __name__ == "__main__":
    main()
