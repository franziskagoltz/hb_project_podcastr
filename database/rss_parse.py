"""temporary file to get the rss feeds and practice with the data we get back.
    will get turned into a text file with all urls and loading and parsing the data when
    the load_db file is being called"""

import feedparser


# planet_money = feedparser.parse("planet_money.xml") 
#local file to speed up inserting data while testing
planet_money = feedparser.parse("http://www.npr.org/rss/podcast.php?id=510289")
freakonomics = feedparser.parse("http://feeds.feedburner.com/freakonomicsradio")
this_american_life = feedparser.parse("http://feed.thisamericanlife.org/talpodcast")
serial = feedparser.parse("http://feeds.serialpodcast.org/serialpodcast")
npr_politics = feedparser.parse("http://www.npr.org/rss/podcast.php?id=510310")
ted_radio_hour = feedparser.parse("http://www.npr.org/rss/podcast.php?id=510298")
sixty_minutes = feedparser.parse("https://api.radio.com/v2/podcast/rss/831?format=MP3_128K")
in_the_dark = feedparser.parse("http://feeds.publicradio.org/public_feeds/in-the-dark/itunes/rss")
accused = feedparser.parse("http://feeds.soundcloud.com/users/soundcloud:users:234220545/sounds.rss")
bcc_news = feedparser.parse("http://www.bbc.co.uk/programmes/p02nq0gn/episodes/downloads.rss")
pbs_newshour = feedparser.parse("http://feeds.feedburner.com/NewsHourHeadlinesPodcast")
sidedoor = feedparser.parse("https://rss.art19.com/sidedoor")
how_to_be_awesome_at_your_job = feedparser.parse("http://awesomeatyourjob.libsyn.com/rss")


rss_feeds = [planet_money, freakonomics, this_american_life, serial, npr_politics, ted_radio_hour,
             sixty_minutes, in_the_dark, accused, bcc_news, pbs_newshour, sidedoor, how_to_be_awesome_at_your_job]

# print planet_money["url"]

# get tags/keywords, i.e business. This is a list of dictionaries (tags being a
# # dict and term a key in its dicts)
# planet_money["feed"]["tags"][0].term  # or: planet_money.feed.tags[0].term

# freakonomics["feed"]["tags"][0].term

# # get link from a particular podcast instance:
# planet_money["items"][0].links
# planet_money["items"][0].links[0]["href"]  # actual link as unicode http website

# get all podcast items:
# planet_money.items()


# example output
# In [3]: for item in planet_money:
#    ...:     print item
#    ...:
# feed
# encoding
# bozo
# version
# namespaces
# entries

# In [10]: for i in planet_money["items"][0]:
#     ...:     print i
#     ...:
# summary_detail
# subtitle
# author
# published_parsed
# title
# author_detail
# image
# rights
# itunes_explicit
# summary
# content
# guidislink
# title_detail
# link
# published
# authors
# rights_detail
# subtitle_detail
# links
# id
# itunes_duration

# In [11]: for i in planet_money["feed"]:
#     ...:     print i
#     ...:
# subtitle
# updated_parsed
# links
# image
# updated
# rights_detail
# summary
# generator
# title
# title_detail
# summary_detail
# itunes_block
# tags
# generator_detail
# link
# authors
# author_detail
# publisher_detail
# language
# rights
# author
# subtitle_detail
