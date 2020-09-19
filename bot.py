import dotenv
import os
import settings
from pprint import pprint
from classes.Fetch import Fetch
import json
import time
# define config variables
credentials = {
    'api_key': os.getenv('API_KEY'),
    'api_secret': os.getenv('API_SECRET'),
    'access_token': os.getenv('ACCESS_TOKEN'),
    'access_secret': os.getenv('ACCESS_SECRET')

}
LAST_ATTENDED_ID_FILE_NAME = os.getenv('FILE_NAME')

fetch = Fetch(credentials)

#run infinitely but rest for 20s
while True:
    fetch.replyToMentions(LAST_ATTENDED_ID_FILE_NAME)
    time.sleep(20)
    print("result.....................")

