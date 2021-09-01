# Emailer
# Author: Tyler Gamvrelis
# Sources:
#     https://github.com/kootenpv/yagmail

import json
import keyring
import logging
import yagmail


EMAIL_INFO_FNAME = 'email_info.json'


class Emailer:

    def __init__(self):
        self._username = None
        self._dest_addr = None
        self._logger = logging.getLogger(__name__)
        self._load_info()
        self._yag = yagmail.SMTP(self._username)

    def _load_info(self):
        with open(EMAIL_INFO_FNAME) as f:
            data = json.load(f)
            self._username = data['gmail_username']
            self._dest_addr = data['dest_address']
            self._logger.info(
                f'Sending emails from {self._username}@gmail.com '
                f'to {self._dest_addr}'
            )

    def save_credentials_if_needed(self):
        if keyring.get_credential('yagmail', username=self._username) is None:
            subject = 'PS5 Stock Helper Test Email'
            body = 'This is a test to verify that email notifications are '\
                   'set up properly. If you\'ve received this then you\'re '\
                   'good to go!'
            self._yag.send(self._dest_addr, subject, contents=body)

    def send_drop_message(self, result):
        subject = f'PS5 Stock Helper - {result.info}'
        body = ''
        body += f'Date: {result.date}\n'
        body += f'Info: {result.info}\n'
        body += 'Links:\n'
        for link in result.links:
            body += f'\t<a href="{link}">{link}</a>\n'
        self._yag.send(self._dest_addr, subject, contents=body)
        self._logger.debug(f'Sent email to {self._dest_addr}')
