# Stock tracker base class

from threading import Thread, Event, Semaphore
import logging

class StockTracker(Thread):
    def __init__(self, group=None, target=None, name=None):
        super(StockTracker, self).__init__(group=group, target=target, name=name)
        self._name = name
        self._stock_check_sem = Semaphore(0)
        self._stop_event = Event()
        self._callback = self._default_callback()

    def stop(self):
        """
        Prevents any more stock checks from executing, and causes the thread to
        exit when the current request (if any) is done executing.
        """
        self._stop_event.set()
        self.request_stock_check() # So that thread isn't blocked
        logging.info('Stop requested')

    def _has_stopped(self):
        """Check whether this thread has been stopped."""
        return self._stop_event.is_set()

    def request_stock_check(self):
        """Unblocks stock checker."""
        if not self._has_stopped():
            self._stock_check_sem.release()

    def set_callback(self, callback):
        """Attaches a function to be called after a stock check is preformed."""
        self._callback = callback

    def _default_callback(self):
        """Default callback function for processing stock check results."""
        logging.warning("Callback unimplemented for tracker \"{0}\"".format(self._name))

    def _do_stock_check(self):
        """
        Performs the stock check.

        Returns:
            None if no new stock, else a populted DropResult.
        """
        if type(self) is StockTracker:
            raise Exception('StockTracker is an abstract class and cannot be instantiated directly')

    def run(self):
        self._stock_check_sem.acquire()
        if self._has_stopped():
            return
        result = self._do_stock_check()
        self._callback(result)

class DropResult:
    def __init__(self, date, links, info):
        self.date = date
        self.links = links
        self.info = info
