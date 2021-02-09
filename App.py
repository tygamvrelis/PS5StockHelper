#!/usr/bin/python
# App to help get a PS5

import time
from AppUtils import *
from LbabinzTracker import *

def stock_check_callback(result):
    # TODO: implement callback function for processing stock check results.
    # Should check for duplicates and open browser if no dups detected
    print(result)

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

    trackers = []
    trackers.append(LbabinzTracker())
    # TODO: implement NowInStockTracker
    # trackers.append(NowInStockTracker())
    for tracker in trackers:
        tracker.set_callback(stock_check_callback)
        tracker.start()

    try:
        while True:
            # At the start of each period, tell each tracker to perform a stock
            # check. Handling of results is dealt with in the callback function
            logging.info("Requesting stock check...")
            for tracker in trackers:
                tracker.request_stock_check()
            time.sleep(period)

    except KeyboardInterrupt as e:
        print("Interrupted: {0}".format(e))
        # Clean up trackers
        for tracker in trackers:
            tracker.stop()
        for tracker in trackers:
            tracker.join()
        logging.info("Exiting...")

if __name__ == "__main__":
    main()
    sys.exit(0)
    