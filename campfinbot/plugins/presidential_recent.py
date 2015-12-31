import json
import requests

import campfinbot
from campfinbot import utils

outputs = []
crontable = []
crontable.append([30, "presidential_recent"])

def presidential_recent():
    """
    Gets a list of recent filings.
    Processes those filings looking for new ones.
    Returns Slack-formatted messages if something is new.
    """

    if campfinbot.LOAD_COMMITTEES:
        candidates = [utils.format_candidate(c) for c in json.loads(requests.get(campfinbot.CANDIDATES_URL).content)['results']]
        utils.load_committees(
            campfinbot.MONGODB_DATABASE.presidential_committees,
            [a['campaign_committee'] for a in candidates])

    recent_filings = json.loads(requests.get(campfinbot.CANDIDATE_FILINGS_URL).content)['results']

    messages = utils.load_filings(
        campfinbot.MONGODB_DATABASE.presidential_filings,
        [c['committee_id'] for c in campfinbot.MONGODB_DATABASE.presidential_committees.find()],
        recent_filings,
        alert=True)

    for message in messages:
        outputs.append([campfinbot.CHANNEL,message])
