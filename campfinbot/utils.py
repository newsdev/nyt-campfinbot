import humanize

import campfinbot
import json
import requests
import sys

import logging

def format_candidate(c):
    """
    Returns an object with a single campaign committee and a list
    of associated PACs and SuperPACs, each formatted properly.
    Used for identifying if a given filing should be alerted or not.
    """
    payload = {}
    payload['campaign_committee'] = {"candidate_name": c['name'], "candidate_id": c['candidate_id'], "committee_name": c['name'] + "'s campaign committee", "committee_id": c["committee_id"]}

    payload['associated_committees'] = []
    for a in c['allpacs']:
        payload['associated_committees'].append({"candidate_name": c['name'], "candidate_id": c['candidate_id'], "committee_name": a['committee_name'], "committee_id": a['fec_id']})
    return payload

def load_committees(collection, committees):
    """
    Given a collection and a list of committees, will insert
    new committees into the collection.
    """
    collection.remove()
    for c in committees:
        if not collection.find_one({"committee_id": c["committee_id"]}):
            collection.insert(c)


def load_filings(collection, committees, recent_filings, alert=False):
    """
    Given a collection of filings, a list of committees, and a list of filings, will insert
    new filings into the collection.
    Returns a list of messages if alert has been set to True.
    """
    messages = []
    for filing in recent_filings:
        if filing['fec_id'] in committees:
            if not collection.find_one({'filing_id': filing['filing_id']}):
                form_type = filing['form_type'].rstrip('HSPAX')
                if form_type in campfinbot.ACCEPTABLE_FORMS:
                    collection.insert(filing)
                    if form_type in campfinbot.ALERT_FORMS and alert:
                        message = "*{comm}* has filed a {form_type}".format(comm=filing['committee_name'],
                                                                                 form_type=filing['form_type'])
                        if filing['is_amendment']:
                            message += " AMENDMENT"
                        
                        message += "on {date}.\n{url}".format(date=filing['filed_date'], url=filing['source_url'])
                        if filing['has_cycle_totals']:
                            try:
                                message += "\n\tReceipts: $%s" % humanize.intcomma(round(float(filing['period_total_receipts']), 2))
                            except:
                                message += "\n\tReceipts: %s" % filing['period_total_receipts']

                            try:
                                message += "\n\tCash on hand: $%s" % humanize.intcomma(round(float(filing['coh_end']), 2))
                            except:
                                message += "\n\tCash on hand: %s" % filing['coh_end']

                            try:
                                message += "\n\tDisbursements: $%s" % humanize.intcomma(round(float(filing['period_total_disbursements']), 2))
                            except:
                                message += "\n\tDisbursements: %s" % filing['period_total_disbursements']

                        messages.append(message)

    return messages

def load_json(endpoint, tries=5):
    i = 0
    while i < tries:
        try:
            return json.loads(requests.get(endpoint).content)['results']
        except Exception as e:
            err = e
        i += 1
    logging.warning("Failed to load endpoint {tries} times, got error {err}".format(tries=tries, err=err))
    return []