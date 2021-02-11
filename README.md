# PS5StockHelper
Helps with getting a PS5.

The idea is you run this, and once there's stock your browser will automatically open the site you can purchase the item from. If you already have desktop notifications and/or Twitter notifications set up, this may not be useful for you. For the latter case, if you don't want to check whether the Tweets you're being notified about actually relate to PS5s, then this could add value.

To be clear: this is NOT a bot to help you get through checkout quickly. That part's on you.

As of now, this app checks the following sites for stock:
- Lbabinz's Twitter feed for PlayStation 5 tweets
- The Sony PlayStation 5 CA Tracker on nowinstock.net

Since this app doesn't go to the retailers (e.g., Best Buy) directly, it doesn't need to worry about rotating user agents, nor do you need to worry about your IP address getting blocked.

FYI: there are probably lots of edge cases I'm not handling. I just wanted something quick that would get the job done. If you can make it better, feel free to fork or submit a PR. Also, this is only focused on Canadian stock, although in principle it could easily be changed to work for stock in other countries too.

# Requirements
You need Python 3.8 so that the snscrape Python API will work. Has only been tested on Windows 10.
