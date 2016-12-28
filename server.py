"""Podcast Radio."""

from jinja2 import StrictUndefined

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound

from flask import Flask, jsonify, render_template, redirect, request, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Podcast, Tag, TagChannel, User, ListeningHistory

from datetime import datetime

import server_functions


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# testing mode false unless specified when the server is run
JS_TESTING_MODE = False

@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


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
    """Signs user up"""

    user_info = request.form

    server_functions.add_user(user_info)

    flash("You are now signed up!")

    return redirect("/podcasts")


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
        current_user = server_functions.get_current_user(email, password)
        flash("You are now logged in!")
        session["user_id"] = current_user.user_id
        session["user_name"] = current_user.name

        return redirect("/podcasts")

    except NoResultFound:
        flash("email and password didn't match any of our records")
        return redirect("/login")


@app.route("/logout")
def logout():
    """handles user logout"""

    session.clear()
    flash("You are now logged out!")

    return redirect("/")


@app.route("/userprofile")
def user_profile():
    """displays user info stored in profile"""

    user_id = session.get("user_id")

    if user_id:

        user = server_functions.get_user(user_id)

        history = server_functions.get_recent_history(user_id)

        skip_like = server_functions.get_skipped_and_likes(user_id)

        return render_template("/user_profile.html", user=user, history=history, skip_like=skip_like)
    else:
        flash("You must be logged in to see your profile.")
        return redirect("/")


@app.route("/podcasts")
def show_podcasts():
    """test page to display all podcasts"""

    return render_template("show_podcasts.html")


@app.route("/record", methods=["POST"])
def record_podcast():
    """records the podcast the user listens to"""

    user_id = session["user_id"]
    podcast_id = int(request.form.get("data"))
    skip = request.form.get("skip")
    love = request.form.get("love")

    if skip:
        skip = True
    if love:
        love = True

    server_functions.record_history(user_id, podcast_id, skip, love)

    return jsonify({"status": "Success!"})


@app.route("/get-content.json")
def get_podcasts():
    """gets podcasts from server"""

    category = str(request.args.get("category"))
    offset = int(request.args.get("offset"))

    tag_ids = server_functions.get_tag_ids(category)

    channel_ids = server_functions.get_channel_ids(tag_ids)

    return server_functions.get_podcasts(channel_ids, offset)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app, "postgresql:///podcastradio")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True


    app.run(host="0.0.0.0")
