"""Utility file: continuesly adds newest released podcasts to the database"""


from model import Channel
import load_db
from model import connect_to_db

from flask import Flask
import feedparser

app = Flask(__name__)


def get_channel_urls():
    """returns all the podcast channel urls stored in the db as a list"""

    all_channels = Channel.query.all()

    return [channel.channel_url for channel in all_channels]


# gets newest episodes from channel rss feed
def get_newest():
    """Loops over channel urls in db and grabs the newest podcasts"""

    all_channel_urls = get_channel_urls()

    for channel_url in all_channel_urls:
        print channel_url
        # get associated channel object
        channel = Channel.query.filter_by(channel_url=channel_url).one()

        etag = channel.channel_etag
        modified = channel.channel_modified
        channel_id = channel.channel_id

        if etag:
            print "Updating the DB based on etags"
            newest_feed = feedparser.parse(channel_url, etag=etag, modified=modified)
            load_db.load_podcasts(newest_feed, channel_id)


if __name__ == "__main__":
    # running when file gets called directly

    connect_to_db(app, "postgresql:///podcastradio")

    get_newest()
