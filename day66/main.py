"""Code responsible for running the Flask server."""
import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)


# Cafe table configuration
class Cafe(db.Model):
    """Create a Cafe table inheriting from SQLAlchemy."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Transform the whole table in a dictionary."""
        # Method 1 - For loop
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry where the key is the column name
            # and the value is its value
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

    # Method 2 - Dictionary comprehension
    # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Home page."""

    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    """Return a random cafe in JSON form."""

    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)

    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all", methods=["GET"])
def get_all_cafes():
    """Return all cafes in the database in JSON form."""

    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()

    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search", methods=["GET"])
def get_cafe_at_location():
    """Return all cafes at the location query in JSON form."""

    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # This might get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

    return (
        jsonify(
            error={"Not found": "Sorry, we couldn't find a cafe at that location."}
        ),
        404,
    )


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
