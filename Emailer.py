# Emailer
# Author: Tyler Gamvrelis
# Sources:
#     https://github.com/kootenpv/yagmail

# Standard library imports
import json
import logging

# Third party imports
import keyring
import yagmail


# Globals
logger = logging.getLogger(__name__)


class EmailInfoLoader:
    FNAME = 'email_info.json'

    def __init__(self):
        self.username = None
        self.dest_addr = None
        self._load_info()

    def _load_info(self):
        with open(EmailInfoLoader.FNAME) as f:
            data = json.load(f)
            self.username = data['gmail_username']
            self.dest_addr = data['dest_address']
            logger.info(
                f'Sending emails from {self.username}@gmail.com '
                f'to {self.dest_addr}'
            )


class Emailer:

    def __init__(self):
        self._info = EmailInfoLoader()
        self._yag = yagmail.SMTP(self._info.username)


    def save_credentials_if_needed(self):
        if keyring.get_credential('yagmail', username=self._info.username) is None:
            subject = 'PS5 Stock Helper Test Email'
            body = 'This is a test to verify that email notifications are '\
                   'set up properly. If you\'ve received this then you\'re '\
                   'good to go!'
            self._yag.send(self._info.dest_addr, subject, contents=body)

    def send_drop_message(self, result):
        subject = f'PS5 Stock Helper - {result.info}'
        body = ''
        body += f'Date: {result.date}\n'
        body += f'Info: {result.info}\n'
        body += 'Links:\n'
        for link in result.links:
            body += f'\t<a href="{link}">{link}</a>\n'
        self._yag.send(self._info.dest_addr, subject, contents=body)
        logger.debug(f'Sent email to {self._info.dest_addr}')
