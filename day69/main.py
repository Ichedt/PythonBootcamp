"""Code responsible for running the Flask server."""
from datetime import date
from functools import wraps
from flask import Flask, abort, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

# Import forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap5(app)


# CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    """Table for posts data."""

    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # Foreign Key related to user ID
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Relationship to the users posts
    author = relationship("User", back_populates="posts")
    img_url = db.Column(db.String(250), nullable=False)
    # Relationship to the users comments
    comments = relationship("Comment", back_populates="parent_post")


class User(UserMixin, db.Model):
    """Table for registered users data."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # Relationship related to this users posts, id is the author of the post
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class Comment(db.Model):
    """Table for comments data."""

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    # Relationship related to the user id author of the comment
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Relationship to the post commented
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


# Set up Flask Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Load user in the application."""

    return db.session.get(User, user_id)


# Admin only decorator
def admin_only(f):
    """Function wrapper to require user to be admin."""

    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise, continue
        return f(*args, **kwargs)

    return decorated_function


# Generating profile images for comment section
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    deafult="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user page."""
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        )
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        hash_and_salt_pw = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8,
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salt_pw,
        )
        db.session.add(new_user)
        db.session.commit()
        # Login registered user
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        # Email does not exist
        if not user:
            flash("That email does not exist. Please try again.")
            return redirect(url_for("login"))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash("Password incorrect. Please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout")
def logout():
    """Log out current user."""
    logout_user()

    return redirect(url_for("get_all_posts"))


@app.route("/")
def get_all_posts():
    """Home page, show all posts."""
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    """Show selected post."""
    requested_post = db.session.get(BlogPost, post_id)
    comment_form = CommentForm()
    # Allow only logged in users
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template(
        "post.html",
        post=requested_post,
        current_user=current_user,
        form=comment_form,
    )


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """Write a new post."""
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """Edit the selected post."""
    post = db.session.get(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template(
        "make-post.html", form=edit_form, is_edit=True, current_user=current_user
    )


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """Delete the selected post."""
    post_to_delete = db.session.get(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    """About page."""

    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    """Contact page."""

    return render_template("contact.html", current_user=current_user)


def main():
    """Run the main code."""
    app.run(debug=False, port=5002)


if __name__ == "__main__":
    main()
