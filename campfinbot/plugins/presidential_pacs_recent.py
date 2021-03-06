
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

    if campfinbot.LOAD_COMMITTEES:
        committees = [utils.get_committee(c) for c in utils.load_json(campfinbot.COMMITTEE_URL)]

        utils.load_committees(
            campfinbot.MONGODB_DATABASE.presidential_committees,
            committees)

    recent_filings = utils.load_json(campfinbot.PAC_FILINGS_URL)

    messages = utils.load_filings(
        campfinbot.MONGODB_DATABASE.presidential_filings,
        campfinbot.MONGODB_DATABASE.presidential_committees.find(),
        recent_filings,
        alert=True)

    for message in messages:
        outputs.append([campfinbot.CHANNEL,message])
