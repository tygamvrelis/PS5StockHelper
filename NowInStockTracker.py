# Checks for drops on https://www.nowinstock.net/ca/videogaming/consoles/sonyps5/
# Author: Tyler Gamvrelis
# Sources:
#    https://medium.com/@speedforcerun/python-crawler-http-error-403-forbidden-1623ae9ba0f

from datetime import datetime, timezone
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

from StockTracker import *


class NowInStockTracker(StockTracker):
    """
    Checks for drops on nowinstock.net.

    Test mode: pretends that one of the entries on the site's status table says
    "In Stock".
    """
    
    def __init__(self):
        super(NowInStockTracker, self).__init__(name='NowInStock_thread')
        self._url = 'https://www.nowinstock.net/ca/videogaming/consoles/sonyps5/'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self._trackers = None

    def _is_in_stock(self, status):
        """Checks whether the given status means the item is in stock."""
        return status != 'Out of Stock'

    def _do_stock_check(self):
        # Scrape the web page for stock info
        req = Request(self._url, headers=self._headers)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        tds = soup.find_all('td', class_='stockStatus')
        trackers = {}
        for td in tds:
            status = td.string
            link = td.parent.a.get('href')
            text = td.parent.a.text
            trackers[text] = (status, link)
        if not self._trackers:
            self._trackers = trackers.copy()

        if self._is_test_mode:
            # Drop first item
            for k, v in trackers.items():
                trackers[k] = ('In Stock', v[1])
                break

        # Compare current stock info to known stock info. Assume keys don't
        # change in time
        nothing_new = True
        for k, v in trackers.items():
            in_stock = self._is_in_stock(v[0])
            if in_stock and not self._is_in_stock(self._trackers[k][0]):
                # There's a new drop!
                nothing_new = False
                link = v[1]
                text = k
            self._trackers[k] = v # Update state

        if nothing_new:
            return None
        else:
            return DropResult(datetime.now(timezone.utc), [link], text)
