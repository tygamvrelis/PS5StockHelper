# Checks for drops on https://twitter.com/Lbabinz
# Sources:
#    https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af

from datetime import datetime, date
import snscrape.modules.twitter as sntwitter
from StockTracker import *

class LbabinzTracker(StockTracker):
    def __init__(self, start_time):
        super(LbabinzTracker, self).__init__(name="Lbabinz_thread")
        self._start_time = start_time
        self._filters = ['PlayStation 5']
        self._filters = [filt.lower() for filt in self._filters] # Automate this, just in case
        self._window = 100 # Maximum number of tweets to pull at a time
        self._last_match = {}
        self._last_tweet_time = None

    def _tweet_is_ps5_drop(self, tweet):
        """Returns True if tweet is detected to be a PS5 drop, else False."""
        for filt in self._filters:
            if filt in tweet.content.lower():
                return True
        return False

    def _do_stock_check(self):
        # Make a scraper and check the tweets within the window. Note that the
        # Python API for snscrape doesn't give us many options, for example, as
        # of this writing, we get batches of tweets 100 at a time. If we were to
        # use the CLI for snscrape, we could change this so we only retrieve as 
        # many tweets as specified in the window, then read in the JSON output. 
        # This could be considered as a future improvement
        match = {}
        scraper = sntwitter.TwitterUserScraper('Lbabinz')
        for i,tweet in enumerate(scraper.get_items()):
            if i > self._window or len(match) != 0:
                break
            # Update most recent Tweet time. If there are no new Tweets since
            # our last check, then break
            if i == 0:
                if not self._last_tweet_time or tweet.date > self._last_tweet_time:
                    self._last_tweet_time = tweet.date
                else:
                    break
            # Check whether this tweet is older than the start time of the app.
            # If so, we can break
            if tweet.date < self._start_time:
                break
            # If we make it here, then there's a new tweet. Let's check this
            # tweet to see if it's a PS5 drop
            if self._tweet_is_ps5_drop(tweet):
                match['id'] = tweet.id
                match['date'] = tweet.date
                if not isinstance(tweet.outlinks, list):
                    tweet.outlinks = [tweet.outlinks]
                match['links'] = tweet.outlinks
                match['content'] = tweet.content
                self._logger.info('Found match!')
        if len(match) == 0:
            return None
        else:
            self._last_match = match
            return DropResult(match['date'], match['links'], match['content'])
