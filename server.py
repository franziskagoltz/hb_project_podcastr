"""Podcast Radio."""

from jinja2 import StrictUndefined

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Podcast, Tag, TagChannel, User, ListeningHistory

from datetime import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route("/")
def index():
    """Landing Page."""

    return render_template("homepage.html")


@app.route("/signup")
def sign_up():
    """User sign up page"""

    return render_template("sign_up.html")


@app.route("/signup", methods=["POST"])
def confirm_signup():
    """Confirms user sign-up"""

    name = request.form.get("name")
    email = request.form.get("email_address")
    password = request.form.get("password")
    age = int(request.form.get("age"))
    sex = request.form.get("sex")
    zipcode = request.form.get("zipcode")

    user = User(name=name, email=email, password=password,
                age=age, sex=sex, zipcode=zipcode)

    db.session.add(user)

    db.session.commit()

# experiment with **kwargs

    session["user_id"] = user.user_id

    flash("You are now signed up!")

    return redirect("/")


@app.route("/login")
def login():
    """Display login page"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def validate_login():
    """Validates login"""

    email = request.form.get("email_address")
    password = request.form.get("password")

    try:
        current_user = User.query.filter(User.email == email, User.password == password).one()
        flash("You are now logged in!")
        session["user_id"] = current_user.user_id

        return redirect("/")

    except NoResultFound:
        flash("email and password didn't match any of our records")
        return redirect("/login")


@app.route("/logout")
def logout():
    """handles user logout"""

    session.clear()
    flash("You are now logged out!")

    return redirect('/')


@app.route("/userprofile")
def user_profile():
    """displays user info stored in profile"""

    user_id = session["user_id"]

    user = User.query.get(user_id)

    return render_template("/user_profile.html", user=user)


@app.route("/podcasts")
def show_podcasts():
    """test page to display all podcasts"""

    return render_template("show_podcasts.html")


@app.route("/record", methods=["POST"])
def record_podcast():
    """records the podcast the user listens to"""

    podcast_id = int(request.form.get("data"))
    user_id = session["user_id"]
    listened_at = datetime.now()

    history = ListeningHistory(podcast_id=podcast_id, user_id=user_id, listened_at=listened_at)

    db.session.add(history)

    db.session.commit()

    return jsonify({"status": "Success!"})


@app.route("/get-content.json")
def get_podcasts():
    """gets podcasts from server"""

    category = str(request.args.get("category"))
    offset = int(request.args.get("offset"))

    # get tag ID for category selected
    search_term = "%{}%".format(category)
    tag_ids = Tag.query.filter(Tag.category.like(search_term)).all()

    all_channels = []

    for tag in tag_ids:

        all_channels.extend(tag.channels)

    # get associated channels:
    channel_ids = [channel.channel_id for channel in all_channels]

    all_podcasts = []

    all_episodes = Podcast.query.filter(Podcast.channel_id.in_(channel_ids))
    newest_first = all_episodes.order_by(desc(Podcast.released_at))
    two_newest_from_offset = newest_first.limit(2).offset(offset).all()

    for episode in two_newest_from_offset:
        podcast = {}

        # populating the dictionary
        podcast["podcast_id"] = episode.podcast_id
        podcast["play_url"] = episode.play_url
        podcast["title"] = episode.title
        podcast["author"] = episode.author

        # appending the podcast dict to our list of dicts
        all_podcasts.append(podcast)

    # creating a dict to pass to frontend via jsonify
    json_dict = {"data": all_podcasts}

    return jsonify(json_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
