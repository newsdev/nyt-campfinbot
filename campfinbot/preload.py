"""
Preloads filings and committees.
Preloaded committees allow us to semi-dynamically associate a set of
committees with a given candidate. This way we can ignore committees
that are not of interest for the 2016 presidential candidates.
Preloaded filings make sure that we don't announce filings that aren't
important.
"""

import campfinbot
import requests
from campfinbot import utils

candidate_filings = utils.load_json(campfinbot.CANDIDATE_FILINGS_URL)
pac_filings = utils.load_json(campfinbot.PAC_FILINGS_URL)
committees = [utils.get_committee(c) for c in utils.load_json(campfinbot.COMMITTEES_URL)]

# Load presidential campaign committees.
utils.load_committees(
    campfinbot.MONGODB_DATABASE.presidential_committees, committees)


# Load filings associated with presidential campaign committees.
utils.load_filings(
    campfinbot.MONGODB_DATABASE.presidential_filings,
    campfinbot.MONGODB_DATABASE.presidential_committees.find(),
    candidate_filings)

# Load filings associated with presidential PACs and SuperPACs.
utils.load_filings(
    campfinbot.MONGODB_DATABASE.presidential_filings,
    campfinbot.MONGODB_DATABASE.presidential_committees.find(),
    pac_filings)