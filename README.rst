Ranked RSS To Twitter Bot
=========================

This script lets you pick articles from the defined
list of RSS feeds classified by statuses selected
twitter users. 

On each run script posts a new status to your 
twitter account in format:

[prefix_message] [article_title] [link_to_article] 

It is recommended to run this script not more than two
times a day since caching of RSS feeds is not implemented.

----------------------------------------------------
DEPENDECIES
----------------------------------------------------

Proven to work with Python v2.7.6 but any Python v2.x 
should be fine. Refer to dependencies below. 

* Pycorpora v0.1.2 https://github.com/aparrish/pycorpora
* Feedparser v5.2.0 https://pypi.python.org/pypi/feedparser
* Tweepy v3.3.0 https://github.com/tweepy/tweepy 

After completing installations above replace default
oceans.json file which supposed to be located in
/usr/local/lib/pythonrX.Y/dist-packages/pycorpora/data/geography
with oceans.json located in bot root directory. 

----------------------------------------------------
CONFIGURATION
----------------------------------------------------

Head over to apps.twitter.com and click "Create New App".

Open "Permissions" tab on application management page
and select option "Read, Write and Access direct messages".

Next, open "Keys and Access Tokens" tab to get all
keys for config.py.

Populate variables in file config.py:

  | C_KEY = ""
  | C_SECRET = ""
  | A_TOKEN = ""
  | A_TOKEN_SECRET = ""

Head over to bitly.com and sign up for account.
When authenticated visit https://bitly.com/a/oauth_apps 
enter your password and hit "Generate token" button.

One the next page copy text under "Generic Access Token"
and copy this string in BITLY_ACCESS_TOKEN var in 
config.py

To add/remove rss/atom feeds or twitter influencers
edit content_config file.

In order to find a feed of any website just post
its url in W3C validator https://validator.w3.org/feed/.
After hitting "Check" button search field will prepopulate 
with url to feed.
Many feeds will not validate but still can be used.

----------------------------------------------------
USAGE
----------------------------------------------------

bot.py --rank-influencers

Run this option first after installation. 
Also, run it every time after you change twitter influencers list 
in content_config.json

bot.py --post-article 
Post title and link of highest scoring article
to twitter.

Files feeds.db and influencers_ranks.db are not meant
to be edited by hand.

----------------------------------------------------
RANKING CALCULATION
----------------------------------------------------

Twitter user influence rank is a composite of following 
products::

  followers_count: 0.7 * num
  retweet_count:   1.0 * num 
  listed_count:    0.2 * num # number of lists on which author name appears

Retweet count is obtained by adding number of retweets for the last
50 statuses.

User with a greatest composite score gets assign 5.0 rank.

Ranks for other twitter users get derived from ratio to top influencer::

  person a total score -> 5.0
  person b total score -> x
  x = (person b * 5.0) / person a  

On every run the script creates classifying collection of words.
These collection gets formed by matching words used by influencers
in last 100 statuses and script own dictionary. 

Script dynamic dictionary consist of mutable set of words in file 
content_config.json and corporas from Corpora project 
https://github.com/dariusk/corpora. Names of corporas utilized: "rooms", 
"countries", "oceans", "seas", "rivers", "us_cities", "us_states", 
"canada_provinces", "canada_territories", "english_cities", "english_towns", 
"venues". Right now there is no configuration for corporas so you will have
to change the code of extend_keywords_set_with_corpora() function in 
pack/textworker.py file.

Formula for word score::

  number_of_occurrences*influencer_0_rank + number_of_occurrences*influencer_1_rank + ... 

Formula for article rank::

  word_0*number_of_occurrences*word_0_score + word_1*number_of_occurrences*word_1_score + ...  
