import os

from pymongo import MongoClient

# F3: Periodic filing.
# F99: Responses to the FEC.
ACCEPTABLE_FORMS = ['F3','F99']

CHANNEL = os.environ.get("CAMPFINBOT_SLACK_CHANNEL", None)
CANDIDATES_URL = "http://%s/campfin/svc/elections/us/v3/finances/2016/president/totals.json" % os.environ.get('CAMPFINBOT_CANDIDATES_HOST', '127.0.0.1:3000')
FILINGS_URL = "http://%s/campfin/svc/elections/us/v3/finances/2016/filings.json" % os.environ.get('CAMPFINBOT_FILINGS_HOST', '127.0.0.1:3000')

MONGODB_CLIENT = MongoClient(os.environ.get('CAMPFINBOT_MONGO_URL', 'mongodb://localhost:27017/'))
MONGODB_DATABASE = MONGODB_CLIENT.campfinbot

#generally we want to load new committees each time we run to keep up to date
#but doing so makes debugging very hard, so you can set this envvar locally
#which will let you add new committees that don't get overwritten
#in order to test specific situations.
LOAD_COMMITTEES = os.environ.get("LOAD_COMMITTEES", True)
if LOAD_COMMITTEES.lower() == 'false':
    #ARG it reads the env var False as a string!!!! fix:
    LOAD_COMMITTEES = False