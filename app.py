import os
import sqlite3
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
load_dotenv()
from werkzeug.security import generate_password_hash, check_password_hash

from database import init_db
from services.tmdb_service import search_movies, get_movie_details
from repositories.users_repo import (
    create_user,
    get_user_by_username
)
from repositories.favorites_repo import (
    add_favorite,
    get_all_favorites,
    is_favorite,
    update_favorite,
    delete_favorite
)
 

app = Flask(__name__)


app.secret_key = os.environ["SECRET_KEY"]

init_db()


# =========================
# MOVIE ROUTES
# =========================

@app.route("/")
def home():
    return render_template("home.html", movies=None)


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()

    if not query:
        flash("Please enter a movie title.")
        return redirect(url_for("home"))

    movies = search_movies(query)

    return render_template(
        "home.html",
        movies=movies,
        query=query
    )


@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = get_movie_details(movie_id)

    if movie is None:
        flash("Movie details could not be loaded.")
        return redirect(url_for("home"))

    favorite_status = False

    if "user_id" in session:
        favorite_status = is_favorite(
            session["user_id"],
            movie_id
        )

    return render_template(
        "movie.html",
        movie=movie,
        is_favorite=favorite_status
    )


# =========================
# FAVORITE ROUTES
# =========================

@app.route("/favorites")
def favorites():
    if "user_id" not in session:
        flash("Please log in to view your favorites.")
        return redirect(url_for("login"))

    movies = get_all_favorites(session["user_id"])

    return render_template(
        "favorites.html",
        movies=movies
    )


@app.route(
    "/favorite/toggle/<int:movie_id>",
    methods=["POST"]
)
def toggle_favorite(movie_id):
    if "user_id" not in session:
        flash("Please log in to save favorites.")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    movie = get_movie_details(movie_id)

    if movie is None:
        flash("Movie details could not be loaded.")
        return redirect(url_for("home"))

    if is_favorite(user_id, movie_id):
        delete_favorite(user_id, movie_id)
        flash("Movie removed from favorites.")

    else:
        add_favorite(user_id, movie)
        flash("Movie added to favorites.")

    return redirect(
        url_for("movie_detail", movie_id=movie_id)
    )


@app.route(
    "/favorite/update/<int:movie_id>",
    methods=["POST"]
)
def refresh_favorite(movie_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    movie = get_movie_details(movie_id)

    if movie is None:
        flash("Movie information could not be updated.")
        return redirect(url_for("favorites"))

    update_favorite(user_id, movie)
    flash("Favorite information updated.")

    return redirect(url_for("favorites"))


@app.route(
    "/favorite/delete/<int:movie_id>",
    methods=["POST"]
)
def remove_favorite(movie_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_favorite(
        session["user_id"],
        movie_id
    )

    flash("Movie removed from favorites.")
    return redirect(url_for("favorites"))


# =========================
# AUTH ROUTES
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if len(username) < 3:
            flash("Username must contain at least 3 characters.")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            create_user(username, password_hash)

        except sqlite3.IntegrityError:
            flash("That username already exists.")
            return render_template("register.html")

        flash("Account created. You can now log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = get_user_by_username(username)

        if user and check_password_hash(
            user["password_hash"],
            password
        ):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("You are now logged in.")
            return redirect(url_for("home"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)