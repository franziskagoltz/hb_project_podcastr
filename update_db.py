"""Utility file: continuesly adds newest released podcasts to the database"""


from model import Channel
import load_db
from model import connect_to_db, db

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
        # print channel_url
        # get associated channel object
        channel = Channel.query.filter_by(channel_url=channel_url).one()

        etag = channel.channel_etag
        modified = channel.channel_modified
        channel_id = channel.channel_id

        if etag:
            print "Updating the DB based on etags"
            print etag
            print modified
            print channel_id

            newest_feed = feedparser.parse(channel_url, etag=etag, modified=modified)

            if newest_feed.status == 200:
                print "newest status", newest_feed.status
                print "newest etag", newest_feed.etag

                load_db.load_podcasts(newest_feed, channel_id)

                # updating the etag and modified values
                channel.channel_etag = newest_feed.etag
                channel.channel_modified = newest_feed.get("modified")

                db.session.commit()

            else:
                print "can't find etag"
                print newest_feed.status

        else:
            print "no etag"

            # newest_feed = feedparser.parse(channel_url, etag=etag, modified=modified)

            # # checking if there are any items in the returned feed
            # if newest_feed.status == 200:
            #     print "newest status", newest_feed.status
            #     print "newest etag", newest_feed.etag
            #     load_db.load_podcasts(newest_feed, channel_id)

            #     # updating the etag and modified values
            #     channel.channel_etag = newest_feed.etag
            #     channel.channel_modified = newest_feed.get("modified")

            #     # db.session.query(Channel).update({Channel.channel_etag: newest_feed.etag})

            #     db.session.commit()
        # elif modified:
        #     "updating db based on modified tag"
        #     newest_feed = feedparser.parse(channel_url, modified=modified)

        #     # checking if there are any items in the returned feed
        #     if newest_feed.status == 200:
        #         load_db.load_podcasts(newest_feed, channel_id)
        #         channel.channel_modified = newest_feed.modified

        


if __name__ == "__main__":
    # running when file gets called directly

    connect_to_db(app, "postgresql:///podcastradio")

    get_newest()
