"""Code responsible for running the Flask server."""
import csv
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config["SECRET_KEY"] = "gsxne7yn7WzWA3"
Bootstrap5(app)


class CafeForm(FlaskForm):
    """Class responsible for creating the form fields."""

    cafe = StringField("Cafe name", validators=[DataRequired()])
    location = StringField(
        "Cafe location on Google Maps (URL)", validators=[DataRequired(), URL()]
    )
    open = StringField("Opening time (e.g. 8AM)", validators=[DataRequired()])
    close = StringField("Closing time (e.g. 6PM)", validators=[DataRequired()])
    coffe_rating = SelectField(
        "Coffee rating",
        choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
        validators=[DataRequired()],
    )
    wifi_rating = SelectField(
        "Wi-Fi strength",
        choices=["❌", "💪", "💪💪", "💪💪💪", "💪💪💪💪💪", "💪💪💪💪💪"],
        validators=[DataRequired()],
    )
    power_rating = SelectField(
        "Power Socket availability",
        choices=["❌", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    """Add Cafe form page."""
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(
                f"\n{form.cafe.data},"
                f"{form.location.data},"
                f"{form.open.data},"
                f"{form.close.data},"
                f"{form.coffe_rating.data},"
                f"{form.wifi_rating.data},"
                f"{form.power_rating.data}"
            )
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    """Cafes page."""
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
