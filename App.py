#!/usr/bin/python
# App to help get a PS5
# Useful:
#    https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af
import snscrape.modules.twitter as sntwitter
from AppUtils import *

def main():
    args = parse_args()
    period = args['period']
    log_level = args['log']
    if log_level != None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(level=numeric_level)
    logging.info('Started app')

    # Creating list to append tweet data to
    tweets_list = []
    filters = ['PlayStation 5']
    filters = [filt.lower() for filt in filters] # Automate this, just in case

    # PoC:
    # TODO: At the start of each period, make a scraper and check the tweets within the window. If any new tweets that match window
    scraper = sntwitter.TwitterUserScraper('Lbabinz')
    for i,tweet in enumerate(sntwitter.TwitterUserScraper('Lbabinz').get_items()):
        if i>100:
            break
        for filt in filters:
            if filt in tweet.content.lower():
                tweets_list.append({'date':tweet.date, 'content':tweet.content, 'links':tweet.outlinks})

    [print(i) for i in tweets_list]

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt as e:
        print("Interrupted: {0}".format(e))
        sys.exit(1)