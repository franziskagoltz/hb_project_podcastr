"""Utility file to seed PodcastRadio database from rss_parse data"""

from sqlalchemy import func
from model import User, ListeningHistory, Tag, Podcast, TagChannel, Channel
# import re
from time import mktime
from datetime import datetime

from model import connect_to_db, db

from flask import Flask
from rss_parse import rss_feeds

app = Flask(__name__)


def load_channels():
    """loads podcast channels into database"""

    print "Channels"

    Channel.query.delete()

    for channel in rss_feeds:
        channel_author = channel["feed"].get("author")
        channel_name = channel["feed"].get("title")
        channel_summary = channel["feed"].get("summary")

        channel = Channel(channel_author=channel_author,
                          channel_name=channel_name,
                          channel_summary=channel_summary,)

        db.session.add(channel)

    db.session.commit()


def load_podcasts():
    """Load podcasts from rss_parse into database."""

    print "Podcasts"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate podcasts
    Podcast.query.delete()

    # rss_feeds = open(data.txt)

    for channel in rss_feeds:

        channel_name = channel["feed"].get("title")

        channel_id = Channel.query.filter_by(channel_name=channel_name).one().channel_id

        for podcast in channel["items"]:
            # iterating through keys in items dict
            all_links = podcast.get("links")
            all_images = podcast.get("image")

            author = podcast.get("author")
            title = podcast.get("title")
            podcast_url = podcast.get("link")
            summary = podcast.get("summary")

            # duration is in a different format for each rss feed, so this uniforms all into seconds
            podcast_duration = podcast.get("itunes_duration")

            if podcast_duration and ":" in podcast_duration.encode('utf-8'):

                splitted = podcast_duration.encode('utf-8').split(":")

                if len(splitted) == 3:
                    hours_to_secs = int(splitted[0]) * 3600
                    mins_to_secs = int(splitted[1]) * 60
                    podcast_duration = hours_to_secs + mins_to_secs + int(splitted[2])

                if len(splitted) == 2:
                    mins_to_secs = int(splitted[0])*60
                    podcast_duration = mins_to_secs + int(splitted[1])

            # converting to a dattime from a python timestruct:
            # http://stackoverflow.com/questions/1697815/how-do-you-convert-a-python-time-struct-time-object-into-a-datetime-object/18726020
            python_timestruct = podcast.get("published_parsed")

            if python_timestruct:
                released_at = datetime.fromtimestamp(mktime(python_timestruct))

            if all_images:
                image_url = all_images.get("href")

            if all_links:
                for link in all_links:
                    if link.type == "audio/mpeg":
                        # checking for type of link so we get the correct url
                        play_url = link.get("href")

            podcast = Podcast(channel_id=channel_id,
                              author=author,
                              title=title,
                              podcast_url=podcast_url,
                              play_url=play_url,
                              released_at=released_at,
                              image_url=image_url,
                              summary=summary,
                              podcast_duration=podcast_duration,)

            # adds instance to the session so it will be stored
            db.session.add(podcast)

    # committing to the database
    db.session.commit()


def load_tags():
    """loads tags into the tags table"""

    print "Tags"

    # deletes all rows in the table so that re-running won't compromise the db
    Tag.query.delete()

    for channel in rss_feeds:

        all_info = channel["feed"].get("tags")

        if all_info:

            #  if tag.query exists : skip, else add

            for collection in all_info:
                category = collection.get("term")

                # checking if the tag is already existent in the db. if so, skip, if not, add

                categories_in_db = Tag.query.filter(Tag.category == category).all()

                if categories_in_db == []:

                    tag = Tag(category=category)

                    db.session.add(tag)

    db.session.commit()


def load_tag_channel_links():
    """populate association table"""

    for channel in rss_feeds:

        channel_name = channel["feed"].get("title")

        channel_id = Channel.query.filter_by(channel_name=channel_name).one().channel_id

        all_tags = channel["feed"].get("tags")

        if all_tags:

            for collection in all_tags:
                category = collection.get("term")

                tag_id = Tag.query.filter_by(category=category).one().tag_id

                tagchannel = TagChannel(channel_id=channel_id, tag_id=tag_id)

                db.session.add(tagchannel)

    db.session.commit()


if __name__ == "__main__":
        # running when file gets called directly

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data to podtcastradio db
    load_channels()
    load_podcasts()
    load_tags()
    load_tag_channel_links()
