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
candidates = [utils.format_candidate(c) for c in utils.load_json(campfinbot.CANDIDATES_URL)]

# Load presidential campaign committees.
utils.load_committees(
    campfinbot.MONGODB_DATABASE.presidential_committees,
    [a['campaign_committee'] for a in candidates])

# Load associated presidential PACs and SuperPACs.
committees = []
for a in candidates:
    committees += a['associated_committees']
utils.load_committees(
    campfinbot.MONGODB_DATABASE.presidential_committees,
    committees)

# Load filings associated with presidential campaign committees.
utils.load_filings(
    campfinbot.MONGODB_DATABASE.presidential_filings,
    [c['committee_id'] for c in campfinbot.MONGODB_DATABASE.presidential_committees.find()],
    candidate_filings)

# Load filings associated with presidential PACs and SuperPACs.
utils.load_filings(
    campfinbot.MONGODB_DATABASE.presidential_filings,
    [c['committee_id'] for c in campfinbot.MONGODB_DATABASE.presidential_committees.find()],
    pac_filings)