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

Once you've downloaded Python 3.8 and the files for this project, the next step is to install the dependencies. To do this, open a terminal in the directory where you downloaded the project files, and run the command `python -m pip install -r requirements.txt`. You should now be good to go!

# Usage
To run this application, open a terminal in the project directory and enter the command `python App.py`. That's it! Now you just wait, and whenever there's a drop an audio track will be played to notify you.

If you want to see a list of usage options, enter `python App.py --help`. For example, you can simulate a drop by entering the command `python App.py --test`.

This app also supports email notifications. To use this feature, you will need a gmail account and will need to [enable less secure apps](https://support.google.com/accounts/answer/6010255?hl=en). Once you've done this, open the `email_info.json` file and fill in the `gmail_username` field with the username of this gmail account. The stock helper app will send emails _from_ this account. Next, fill in the `dest_address` field with the email address that you want stock notification emails _to be sent to_. A made-up example is shown below, which will result in emails being sent _from_ johndoe@gmail.com _to_ foobar@gmail.com:
```json
{
	"gmail_username": "johndoe",
	"dest_address": "foobar@gmail.com"
}
```

With all this done, start the app using the `--email` option, i.e., `python App.py --email`. If it is your first time starting the stock helper app with this gmail account, you will be asked for your password. This password will be stored in your system's [keyring](https://pypi.org/project/keyring/) so that you don't need to enter it next time. If your credentials are valid, then you should receive a test email confirming that email notifications are working. If that's the case, then you should receive an email whenever a drop is detected!

If you accidentally enter your password incorrectly and save it in the keyring, the stock helper won't give you a chance to fix it. As a quick workaround for this, you can clear email credentials saved in the keyring by running the command `python ClearEmailCredentials.py`.
