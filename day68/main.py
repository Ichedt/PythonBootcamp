from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "#JZ3Bnz!h67p*@mD"

# Connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy()
db.init_app(app)

# Set up Flask Login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Create user_loader callback
@login_manager.user_loader
def load_user(user_id):
    """Load user ID to be used in the authentication process."""

    return db.session.get(User, user_id)


# Create the table in database with the UserMixin
class User(UserMixin, db.Model):
    """Create the User database."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Home page."""

    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        email = request.form.get("email")
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        # If user already exists
        if user:
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for("login"))
        # Hash and salt the password
        hash_and_salt_pw = generate_password_hash(
            request.form.get("password"),
            method="pbkdf2:sha256",
            salt_length=8,
        )
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salt_pw,
        )
        db.session.add(new_user)
        db.session.commit()
        # Login user after adding to the database
        login_user(new_user)
        # Pass over the user's name
        return render_template("secrets.html", name=request.form.get("name"))

    # Passing if the user is already logged-in
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login an existing user."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Find user by email
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        # If user doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        # Check password
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("secrets"))

    # Passing if the user is already logged-in
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/secrets")
@login_required
def secrets():
    """Secret page. Accessible after the authentication."""

    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route("/logout")
def logout():
    """Logout the user."""
    logout_user()

    return redirect(url_for("home"))


@app.route("/download")
@login_required
def download():
    """Download the file."""

    return send_from_directory("static", path="files/cheat_sheet.pdf")


def main():
    """Run the main code."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
