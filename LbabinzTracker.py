# Checks for drops on https://twitter.com/Lbabinz
# Sources:
#    https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af

import logging
from datetime import datetime, date
import snscrape.modules.twitter as sntwitter
from StockTracker import *

class LbabinzTracker(StockTracker):
    def __init__(self):
        super(LbabinzTracker, self).__init__(name="Lbabinz_thread")
        self._filters = ['PlayStation 5']
        self._filters = [filt.lower() for filt in self._filters] # Automate this, just in case
        self._window = 5 # Maximum number of tweets to pull at a time
        self._last_match = {}
        self._last_time = None

    def _tweet_is_ps5_drop(self, tweet):
        """Returns True if tweet is detected to be a PS5 drop, else False."""
        for filt in self._filters:
            if filt in tweet.content.lower():
                return True
        return False

    def _do_stock_check(self):
        # Make a scraper and check the tweets within the window
        match = {}
        scraper = sntwitter.TwitterUserScraper('Lbabinz')
        for i,tweet in enumerate(scraper.get_items()):
            if i > self._window or len(match) != 0:
                break
            # Update most recent Tweet time. If there are no new Tweets since
            # our last check, then break
            if i == 1:
                if not self._last_time or tweet.date > self._last_time:
                    self._most_recent_tweet_time = tweet.date
                else:
                    break
            # If we make it here, then there's a new tweet. Let's check this
            # tweet to see if it's a PS5 drop
            if self._tweet_is_ps5_drop(tweet):
                match['id'] = tweet.id
                match['date'] = tweet.date
                match['links'] = tweet.outlinks
                match['content'] = tweet.content
                logging.info('Found match!')

        if len(match) == 0:
            return None
        else:
            self._last_match = match
            return DropResult(match['date'], match['links'], match['content'])
