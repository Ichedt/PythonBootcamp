"""Code responsible for running the Flask server."""
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
HEADERS = {"accept": "application/json"}
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMG_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config["SECRET_KEY"] = "2DTkZ@zdD4rK7#w$wXWn!Ksj"
Bootstrap5(app)

# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy()
db.init_app(app)


# Create table
class Movie(db.Model):
    """Inherit the database model from SQLAlchemy and create a database."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()

# After adding new movie, comment out this code
"""
new_movie = Movie(
    title="Tár",
    year=2023,
    description="Tár is a 2022 psychological drama film written and directed by Todd Field. Cate Blanchett stars as Lydia Tár, a world-renowned conductor facing accusations of misconduct.",
    rating=91,
    ranking=1,
    review="Excellent movie!",
    img_url="https://http2.mlstatic.com/D_NQ_NP_716575-MLB71346728528_082023-O.webp"
)
with app.app_context():
    db.session.add(new_movie)
    db.session.commit()
"""


class RateMovieForm(FlaskForm):
    """Inherit from FlaskWTF the model for the rating form to be displayed."""

    rating = StringField("Rotten Tomatoes rating out of 100")
    review = StringField("Your review")
    submit = SubmitField("Done")


class FindMovieForm(FlaskForm):
    """Inherit from FlaskWTF the model for the adding form to be displayed."""

    title = StringField("Movie title", validators=[DataRequired()])
    submit = SubmitField("Add movie")


@app.route("/")
def home():
    """Home page."""
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()  # Convert ScalarResult to Python List

    for _, i in enumerate(all_movies):
        i.ranking = len(all_movies) - 1
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    """Add movie page."""
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(
            MOVIE_DB_SEARCH_URL,
            params={"query": movie_title},
            headers=HEADERS,
            timeout=10,
        )
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    """Find movie page."""
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        # The language parameter is optional
        response = requests.get(movie_api_id, params={"language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            # The data includes day and month, so edit it off
            year=data["release_data"].split("-")[0],
            img_url=f"{MOVIE_DB_IMG_URL}{data['poster_path']}",
            description=data["overview"],
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("rate_movie", id=new_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    """Edit movie page."""
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete_movie():
    """Delete movie page."""
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))


def main():
    """Run the main code."""
    app.run()


if __name__ == "__main__":
    main()
