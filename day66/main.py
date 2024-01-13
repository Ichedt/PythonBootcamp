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


@app.route("/add", methods=["POST"])
def post_new_cafe():
    """Add a new cafe to the database."""
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"Success": "Successfully added new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    """Update the price of the selected cafe."""
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        # Add the status code after the jsonify method. 200 = Ok
        return jsonify(response={"Success": "Successfully updated the price."}), 200

    # 404 = Not found
    return (
        jsonify(error={"Not found": "Sorry, this cafe was not found in the database."}),
        404,
    )


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == "APIKey":  # Example API key
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return (
                jsonify(
                    response={"Success": "Successfully deleted cafe from database."}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    error={
                        "Not found": "Sorry, this cafe was not found in the database."
                    }
                ),
                404,
            )

    return (
        jsonify(
            error={
                "Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."
            }
        ),
        403,
    )


def main():
    """Run the main code."""
    app.run(debug=False)


if __name__ == "__main__":
    main()
