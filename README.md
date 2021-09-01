# PS5StockHelper
Helps with getting a PS5.

The idea is you run this, and once there's stock your browser will automatically open the site you can purchase the item from. If you already have desktop notifications and/or Twitter notifications set up, this may not be useful for you. For the latter case, if you don't want to check whether the Tweets you're being notified about actually relate to PS5s, then this could add value.

To be clear: this is NOT a bot to help you get through checkout quickly. That part's on you. For the best results, make sure you have your address and payment information saved with the retailers ahead of time.

As of now, this app checks the following sites for stock:
- [Lbabinz's Twitter feed for PlayStation 5 tweets](https://twitter.com/Lbabinz)
- [The Sony PlayStation 5 CA Tracker on nowinstock.net](https://www.nowinstock.net/ca/videogaming/consoles/sonyps5/)

Since this app doesn't go to the retailers (e.g., Best Buy) directly, it doesn't need to worry about rotating user agents, nor do you need to worry about your IP address getting blocked.

FYI: there are probably lots of edge cases I'm not handling. I just wanted something quick that would get the job done. If you can make it better, feel free to fork or submit a PR. Also, this is only focused on Canadian stock, although in principle it could easily be changed to work for stock in other countries too.

# Setup
You need Python 3.8 so that the snscrape Python API will work. Has only been tested on Windows 10.

You can download Python 3.8 here:
- [Windows](https://www.python.org/getit/windows/)
- [MacOS](https://www.python.org/downloads/macos/)

Once you've downloaded Python 3.8 and the files for this project, the next step is to install the dependencies. To do this, open a terminal in the directory where you downloaded the project files, and run the command `pip install -r requirements.txt`. You should now be good to go!

# Usage
To run this application, open a terminal in the project directory and enter the command `python App.py`. That's it! Now you just wait, and whenever there's a drop an audio track will be played to notify you.

If you want to see a list of usage options, enter `python App.py --help`. For example, you can simulate a drop by entering the command `python App.py --test`.