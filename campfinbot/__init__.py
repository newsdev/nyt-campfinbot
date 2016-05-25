import os
import datetime

from pymongo import MongoClient

# F3: Periodic filing.
# F99: Responses to the FEC.
ALERT_FORMS = ['F3','F99', 'F3L'] #forms to alert immediately
ACCEPTABLE_FORMS = ALERT_FORMS + ['F24'] #forms to load into db

CHANNEL = os.environ.get("CAMPFINBOT_SLACK_CHANNEL", None)
COMMITTEE_URL = "{}/api/v1/committees.json".format(os.environ.get('API_BASE', '127.0.0.1:8000'))
CANDIDATE_FILINGS_URL = "{}/api/v1/candidatefilings.json".format(os.environ.get('API_BASE', '127.0.0.1:8000'))
PAC_FILINGS_URL = "{}/api/v1/pacandpartyfilings.json".format(os.environ.get('API_BASE', '127.0.0.1:8000'))

#don't alert forms filed before this date
#prevents alerting old forms when new committees added
EARLIEST_ALERT = (datetime.date.today() - datetime.timedelta(days=4)).strftime('%Y-%m-%d')

#path to file with committees we don't want to alert
EXCLUDED_COMMITTEE_PATH = os.environ.get("EXCLUDED_COMMITTEE_PATH", None)

MONGODB_CLIENT = MongoClient(os.environ.get('CAMPFINBOT_MONGO_URL', 'mongodb://localhost:27017/'))
MONGODB_DATABASE = MONGODB_CLIENT.campfinbot

#generally we want to load new committees each time we run to keep up to date
#but doing so makes debugging very hard because it deletes committees you've
#manually added. so you can set this envvar locally
#which will let you add new committees that don't get overwritten
#in order to test specific situations.
LOAD_COMMITTEES = os.environ.get("LOAD_COMMITTEES", True)
#it reads the env var False as a string!!!! fix:
try:
    load_comm_str = LOAD_COMMITTEES.lower()
except AttributeError:
    pass
else:
    LOAD_COMMITTEES = {"true":True, "false":False}[load_comm_str]