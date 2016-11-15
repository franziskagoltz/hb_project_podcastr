"""test file for podcast radio"""

from unittest import TestCase
from server import app
from model import connect_to_db, db, Podcast, Tag, TagChannel, User, ListeningHistory, Channel
from sqlalchemy import desc
from datetime import datetime


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome to PodcastRadio", result.data)

    def test_listen(self):
        """Test podcast listen page"""

        result = self.client.get("/podcasts")
        self.assertIn("Let's see the podcasts", result.data)
        self.assertIn("Station", result.data)

    def test_signup(self):
        """Test signup page"""

        result = self.client.get("/signup")
        self.assertIn("Sign Up", result.data)

    def test_login(self):
        """Test signup page"""

        result = self.client.get("/login")
        self.assertIn("Login", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///podcastradio")

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def test_userprofile_page(self):
        """Test user profile page."""

        result = self.client.get("/userprofile")
        self.assertIn("User Profile", result.data)

    def test_logged_in(self):
        """Test if correct display of buttons on landing page"""

        result = self.client.get("/")
        self.assertIn("Logout", result.data)
        self.assertNotIn("Login", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config["TESTING"] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_get_podcast(self):
        """Test get podcast query"""

        channel_ids = db.session.query(Channel.channel_id).all()

        offset = 0

        all_episodes_test = Podcast.query.filter(Podcast.channel_id.in_(channel_ids)).all()
        self.assertIn(all_episodes_test[0].author, "NPR")

        all_episodes = Podcast.query.filter(Podcast.channel_id.in_(channel_ids))

        newest_first_test = all_episodes.order_by(desc(Podcast.released_at)).all()
        self.assertEqual(newest_first_test[0].released_at, datetime.strptime("2016-11-10", "%Y-%m-%d"))

        newest_first = all_episodes.order_by(desc(Podcast.released_at))

        two_newest_from_offset = newest_first.limit(2).offset(offset).all()
        self.assertEqual(two_newest_from_offset[0].released_at, datetime.strptime("2016-11-10", "%Y-%m-%d"))

    def test_get_tags(self):
        """Test get tag_ids"""

        search_term = "%{}%".format("News")
        tag_ids = Tag.query.filter(Tag.category.like(search_term)).all()
        self.assertEqual(tag_ids[0].tag_id, 1)

    def test_get_channels(self):
        """Test get channel_ids"""

        tag_ids = Tag.query

        tag_ids_single = [tag.tag_id for tag in tag_ids]

        tag_ids_objects = Tag.query.filter(Tag.tag_id.in_(tag_ids_single)).all()

        all_channels = []

        for tag in tag_ids_objects:
            all_channels.extend(tag.channels)

        channel_ids_objects = db.session.query(Channel.channel_id).all()

        channel_ids = [channel.channel_id for channel in channel_ids_objects]

        self.assertEqual(channel_ids[0], 1)

    def test_get_user(self):
        """Test get user info to display on user profile page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

        result = self.client.get("/userprofile")
        self.assertIn("Jane", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged out of session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_userprofile_page(self):
        """Test that user can't see userprofile page when logged out."""

        result = self.client.get("/userprofile", follow_redirects=True)
        self.assertIn("You must be logged in", result.data)


def example_data():
    """loads example data into the db"""

    db.create_all()

    # Tag Data
    news = Tag(category="News")
    comedy = Tag(category="Comedy")
    tv = Tag(category="TV")

    # User Data
    jane = User(name="Jane", email="jane@gmail.com", password="jane", age=21, sex="female", zipcode="12345")
    debbie = User(name="Debbie", email="debbiw@gmail.com", password="debbie", age=22, sex="female", zipcode="12345")
    tom = User(name="Tom", email="tom@gmail.com", password="tom", age=23, sex="male", zipcode="12345")

    # Channel Data
    pm = Channel(channel_name="Planet Money", channel_author="NPR", channel_summary="This is planet money")
    fr = Channel(channel_name="Freakonomics", channel_author="WNYC", channel_summary="This is Freakonomics")

    db.session.add_all([news, comedy, tv, jane, debbie, tom, pm, fr])
    db.session.commit()

    # Podcast Data
    pm_ep1 = Podcast(channel_id=pm.channel_id, author="NPR", title="#734: The Trump Indicators", podcast_url="podcast_url", play_url="https://play.podtrac.com/npr-510289/npr.mc.tritondigital.com/NPR_510289/media/anon.npr-mp3/npr/pmoney/2016/11/20161109_pmoney_podcast110916.mp3?orgId=1&d=795&p=510289&story=501460703&t=podcast&e=501460703&ft=pod&f=510289",
                     released_at=datetime.strptime("2016-11-10", "%Y-%m-%d"), image_url="", summary="Episode 734", podcast_duration=2345)
    fr_ep1 = Podcast(channel_id=fr.channel_id, author="Freakonomics", title="Who Needs Handwriting?", podcast_url="podcast_url", play_url="http://feedproxy.google.com/~r/freakonomicsradio/~5/t1z4-mI6QYM/freakonomics_podcast021016.mp3",
                     released_at=datetime.strptime("2016-11-04", "%Y-%m-%d"), image_url="", summary="Freak101", podcast_duration=2345)

    db.session.add_all([pm_ep1, fr_ep1])
    db.session.commit()

    # TagChannel Data
    pm_tagChannel = TagChannel(tag_id=news.tag_id, channel_id=pm.channel_id)

    # ListeningHistory Data
    lh1 = ListeningHistory(podcast_id=pm_ep1.podcast_id, user_id=jane.user_id, listened_at="2016-11-14")

    db.session.add_all([pm_tagChannel, lh1])
    db.session.commit()



if __name__ == "__main__":
    import unittest

    unittest.main()
