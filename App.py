#!/usr/bin/python
# App to help get a PS5
# Author: Tyler Gamvrelis

import time
import sys
import threading
from queue import Queue
import webbrowser
from datetime import datetime, timezone
from functools import partial
from AppUtils import *
from LbabinzTracker import *
from NowInStockTracker import *
from AudioNotifier import *

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.readline())

def stock_check_callback(audio_notifier, result):
    # TODO: Consider checking for duplicate drops across trackers within last
    # X seconds
    logger = logging.getLogger(__name__)
    logger.debug(result)
    if result == None:
        return
    logger.info(result.info)
    for link in result.links:
        webbrowser.open(link)
    if audio_notifier:
        audio_notifier.start_audio()

def main():
    args = parse_args()
    period = args['period']
    log_level = args['log']
    mute = args['mute']
    test_mode = args['test']
    logger = logging.getLogger(__name__)
    if log_level != None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig()
        logger.setLevel(numeric_level)
    logger.info('Started app')
    if test_mode:
        logger.info('~~TEST MODE~~')

    audio_notifier = None
    if not mute:
        audio_notifier = AudioNotifier()
        audio_notifier.start()

    trackers = []
    trackers.append(LbabinzTracker(datetime.now(timezone.utc)))
    trackers.append(NowInStockTracker())
    for tracker in trackers:
        tracker.set_callback(partial(stock_check_callback, audio_notifier))
        if test_mode:
            tracker.enable_test_mode()
        tracker.start()

    # https://stackoverflow.com/questions/2408560/python-nonblocking-console-input
    input_queue = Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    try:
        ticks = 0
        while True:
            if ticks % period == 0:
                # At the start of each period, tell each tracker to perform a
                # stock check. Handling of results is dealt with in the callback
                # function
                logger.info(
                    '{0}: Requesting stock checks...'.format(datetime.now())
                )
                for tracker in trackers:
                    tracker.request_stock_check()
            
            # Any user input containing enter stops the audio notification
            if audio_notifier and not input_queue.empty():
                audio_notifier.stop_audio()

            # Bookkeeping
            ticks += 1
            time.sleep(1)

    except KeyboardInterrupt as e:
        print('Interrupted: {0}'.format(e))
        # Clean up trackers
        for tracker in trackers:
            tracker.stop()
        for tracker in trackers:
            tracker.join()
        if audio_notifier:
            audio_notifier.stop()
            audio_notifier.join()
        logger.info('Exiting...')

if __name__ == '__main__':
    main()
    sys.exit(0)
    