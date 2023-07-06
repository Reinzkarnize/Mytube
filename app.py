from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from pytube import Playlist, YouTube
import os

from helpers import apology, login_required

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # Set maximum upload size to 32 megabytes

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mytube.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        url = request.form.get("yt-play-url")
        title = request.form.get("play-title")

        # Checking if user provided the required input
        if not url:
            return apology("must provide playlist URL", 401)
        if not title:
            return apology("must provide playlist title", 401)
        try:
            image = request.files['upload_image']
        except:
            return apology("Upload file error", 401)

        # Checking valid playlist URL
        videos = Playlist(url)

        if not videos:
            return apology("please provide valid URL")

        # Scrape all title from playlist videos
        video_title = []
        for link in videos:
            video_title.append(YouTube(link).title)

        # Write submitted form to playlists database
        db.execute("INSERT INTO playlists (title, user_id) VALUES (?, ?)", title, session['user_id'])

        # Select the newest playlist_id created to update video url and image name
        playlist_id = db.execute("SELECT playlist_id FROM playlists ORDER BY created_at DESC LIMIT 1;")[0][
            'playlist_id']

        # insert playlist videos to database
        for vlink, vtitle in zip(videos, video_title):
            # Convert video URLs to /embed
            vlink = vlink.replace('/watch?v=', '/embed/')
            db.execute("INSERT INTO videos (url, video_title, playlist_id) VALUES (?, ?, ?)", vlink, vtitle,
                       playlist_id)

        # if user provide valid image
        if image:
            # save file as playlist_id name
            file_path = f"static/playlist/{playlist_id}.jpg"
            image.save(file_path)

            # update image name to database
            db.execute("UPDATE playlists SET image = ? WHERE playlist_id = ?", f'{playlist_id}.jpg', playlist_id)

        return redirect("/")

        # return render_template("test.html", url=url, title=title, videos=videos, video_title=video_title)
    else:

        playlists = db.execute("SELECT * FROM playlists WHERE user_id = ?", session['user_id'])

        return render_template("index.html", playlists=playlists)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        userName = request.form.get("username")
        userPassword = request.form.get("password")
        userConfirmation = request.form.get("confirm_password")

        # Ensure username was submitted &
        if not userName:
            return apology("must provide username", 400)

        # Ensure the username already exists/not
        elif db.execute("SELECT username FROM users WHERE username = ?", userName):
            return apology("username already exist", 400)

        # Ensure password was submitted
        elif not userPassword:
            return apology("must provide password", 400)

        # # Ensure confrimation was submitted
        elif not userConfirmation:
            return apology("must provide confirmation password", 400)

        # Ensure password and confirmation password match
        elif userPassword != userConfirmation:
            return apology("passwords do not match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", userName, generate_password_hash(userPassword))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/playlist")
@login_required
def playlist():
    playlist_id = request.args.get('playlist_id')
    playlist_id = int(playlist_id)

    videos = db.execute("SELECT * FROM videos WHERE playlist_id = ?", playlist_id)

    playlists = db.execute("SELECT * FROM playlists WHERE user_id = ?", session['user_id'])

    return render_template("playlist.html", videos=videos, playlists=playlists)


@app.route("/remove")
@login_required
def remove():
    playlist_id = request.args.get('playlist_id')
    playlist_id = int(playlist_id)

    image = db.execute("SELECT image FROM playlists WHERE playlist_id = ?", playlist_id)[0]['image']
    image_path = f"static/playlist/{image}"

    if os.path.exists(image_path):
        os.remove(image_path)

    db.execute("DELETE FROM playlists WHERE playlist_id = ?", playlist_id)
    db.execute("DELETE FROM videos WHERE playlist_id = ?", playlist_id)

    return redirect("/")


@app.route("/settings")
@login_required
def settings():
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])

    playlists = db.execute("SELECT * FROM playlists WHERE user_id = ?", session['user_id'])

    return render_template("settings.html", user_name=user_name, playlists=playlists)


@app.route("/change_usrname", methods=["GET", "POST"])
@login_required
def change_usrname():
    if request.method == "POST":
        userName = request.form.get("new_username")

        if not userName:
            return apology("Must provide new username", 401)

        db.execute("UPDATE users SET username = ? WHERE id = ?", userName, session["user_id"])

        return redirect("/settings")


@app.route("/change_password", methods=["GET", "POST"])
def change_pwd():
    if request.method == "POST":
        new_pwd = request.form.get("new_pwd")

        # Query database for username
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_pwd")):
            return apology("Invalid password")

        # Ensure password was submitted
        elif not new_pwd:
            return apology("must provide new password", 400)

        # Ensure confrimation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Ensure passwords was match
        elif request.form.get("confirmation") != new_pwd:
            return apology("Passwords do not match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_pwd), session["user_id"])

        return redirect("/settings")


if __name__ == "__main__":
    app.run()
