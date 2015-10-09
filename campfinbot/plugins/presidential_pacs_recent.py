import json
import requests

import campfinbot
from campfinbot import utils

outputs = []
crontable = []
crontable.append([30, "presidential_pacs_recent"])

def presidential_pacs_recent():
    """
    Gets a list of recent filings.
    Processes those filings looking for new ones.
    Returns Slack-formatted messages if something is new.
    """
    recent_filings = json.loads(requests.get(campfinbot.FILINGS_URL).content)['results']

    utils.load_filings(
        campfinbot.MONGODB_DATABASE.presidential_pac_filings,
        [c['committee_id'] for c in campfinbot.MONGODB_DATABASE.presidential_pac_committees.find()],
        alert=True)

    for message in messages:
        outputs.append([campfinbot.CHANNEL,message])