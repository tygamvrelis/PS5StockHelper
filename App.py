#!/usr/bin/python
# App to help get a PS5
# Author: Tyler Gamvrelis

import time
import webbrowser
from datetime import datetime, timezone
from AppUtils import *
from LbabinzTracker import *
from NowInStockTracker import *

def stock_check_callback(result):
    # TODO: Consider checking for duplicate drops across trackers within last
    # X seconds
    logger = logging.getLogger(__name__)
    logger.debug(result)
    if result == None:
        return
    logger.info(result.info)
    for link in result.links:
        webbrowser.open(link)

def main():
    args = parse_args()
    period = args['period']
    log_level = args['log']
    logger = logging.getLogger(__name__)
    if log_level != None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig()
        logger.setLevel(numeric_level)
    logger.info('Started app')

    trackers = []
    trackers.append(LbabinzTracker(datetime.now(timezone.utc)))
    trackers.append(NowInStockTracker())
    for tracker in trackers:
        tracker.set_callback(stock_check_callback)
        tracker.start()

    try:
        while True:
            # At the start of each period, tell each tracker to perform a stock
            # check. Handling of results is dealt with in the callback function
            logger.info('{0}: Requesting stock checks...'.format(datetime.now()))
            for tracker in trackers:
                tracker.request_stock_check()
            time.sleep(period)

    except KeyboardInterrupt as e:
        print('Interrupted: {0}'.format(e))
        # Clean up trackers
        for tracker in trackers:
            tracker.stop()
        for tracker in trackers:
            tracker.join()
        logger.info('Exiting...')

if __name__ == '__main__':
    main()
    sys.exit(0)
    