# Clear email credentials saved in keyring
# Author: Tyler Gamvrelis

# Third party imports
import keyring

# Local Application Imports
from Emailer import EmailInfoLoader


info = EmailInfoLoader()
try:
	keyring.delete_password('yagmail', username=info.username + '@gmail.com')
	print('Deleted credentials successfully')
except keyring.errors.PasswordDeleteError:
	print('Error while deleting credentials. '
		  'Are you sure they exist in the keyring?')
