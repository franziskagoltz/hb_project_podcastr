"""Models and database functions for PodcastRadio project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of PodcastRadio website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False) #unique=True
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String(6), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return "User id={} email={} password={} zipcode={}".format(
            self.user_id, self.email, self.password, self.zipcode)


class Channel(db.Model):
    """Podcast Channel details for PodcastRadio website"""

    __tablename__ = "channels"

    channel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_name = db.Column(db.String(200), unique=True, nullable=False)
    channel_author = db.Column(db.String(200), nullable=True)
    channel_summary = db.Column(db.String, nullable=True)
    channel_modified = db.Column(db.String(64), nullable=True)
    channel_etag = db.Column(db.String(100), nullable=True)
    channel_checked = db.Column(db.DateTime, nullable=True)

    tags = db.relationship("Tag", secondary="tags_channels_link", backref="channels")

    def __repr__(self):
        return "channel id={} name={}".format(
            self.channel_id, self.channel_name)


class Podcast(db.Model):
    """ Podcast details for PodcastRadio website"""

    __tablename__ = "podcasts"

    podcast_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.channel_id"), nullable=False)
    author = db.Column(db.String(500), nullable=True)
    title = db.Column(db.String(500), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    podcast_url = db.Column(db.String(500), nullable=True)
    play_url = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.String, nullable=True)
    #check for type text
    image_url = db.Column(db.String(500), nullable=True)
    podcast_duration = db.Column(db.Integer, nullable=True)

    # create DB command: createdb -E UTF8 -T template0 --locale=en_US.utf8 databasename

    def __repr__(self):
        return "Podcast-ID={} Title={} play_url={}".format(
            self.podcast_id, self.title.encode('utf-8'), self.play_url.encode('utf-8'))


class Tag(db.Model):
    """ Category details about podcasts """

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Tag id={} category={}".format(
            self.tag_id, self.category)


class TagChannel(db.Model):
    """ Association table between Tag and Podcast class """

    __tablename__ = "tags_channels_link"

    tp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.channel_id"), nullable=False)

    def __repr__(self):
        return "SPK= {} Tag id={} podcast_id={}".format(
            self.tp_id, self.tag_id, self.channel_id)


class ListeningHistory(db.Model):
    """Keeps track of the ListeningHistory for a certain user """

    __tablename__ = "listening_histories"

    listening_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey("podcasts.podcast_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    listened_at = db.Column(db.DateTime, nullable=False)
    skip = db.Column(db.Boolean, nullable=True)
    love = db.Column(db.Boolean, nullable=True)

    users = db.relationship("User", backref=db.backref("listening_histories", order_by=user_id))

    podcasts = db.relationship("Podcast", backref=db.backref("listening_histories", order_by=podcast_id))

    def __repr__(self):
        return "podcast_id= {} user_id={} listened_at={}".format(
            self.podcast_id, self.user_id, self.listened_at)


##############################################################################
# Helper functions

def connect_to_db(app, database_uri):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # running when file gets called directly

    from server import app
    connect_to_db(app, "postgresql:///podcastradio")
    print "Connected to DB."
