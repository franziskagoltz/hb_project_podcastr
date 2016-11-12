"""functions for server.py"""

from model import connect_to_db, db, Podcast, Tag, User, ListeningHistory
from flask import Flask, jsonify, session
from sqlalchemy import desc
from datetime import datetime


def get_current_user(email, password):
    """getting the current user from the database"""

    return User.query.filter(User.email == email, User.password == password).one()


def get_user(user_id):
    """queries db for user by id"""

    return User.query.get(user_id)


def add_user(user_info):
    """adds a new user to the database"""

    for data in user_info:
        name = user_info.get("name")
        email = user_info.get("email_address")
        password = user_info.get("password")
        age = user_info.get("age")
        sex = user_info.get("sex")
        zipcode = user_info.get("zipcode")

        if age.encode("utf-8") != "":
            age = int(age)
        else:
            age = None

    user = User(name=name, email=email, password=password,
                age=age, sex=sex, zipcode=zipcode)

    db.session.add(user)

    db.session.commit()

    # logs user in upon signup
    session["user_id"] = user.user_id


def get_podcasts(channel_ids, offset):
    """Queries the database for podcasts based on selected category"""

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


def get_tag_ids(category):
    """gets tag ids of the tags associated with selected category"""

    search_term = "%{}%".format(category)
    tag_ids = Tag.query.filter(Tag.category.like(search_term)).all()

    return tag_ids


def get_channel_ids(tag_ids):
    """gets channels associated with the selected category"""

    all_channels = []

    for tag in tag_ids:

        all_channels.extend(tag.channels)

    # get associated channels:
    channel_ids = [channel.channel_id for channel in all_channels]

    return channel_ids


def record_history(user_id, podcast_id):
    """records the user listening history"""

    listened_at = datetime.now()

    history = ListeningHistory(podcast_id=podcast_id, user_id=user_id, listened_at=listened_at)

    db.session.add(history)

    db.session.commit()
