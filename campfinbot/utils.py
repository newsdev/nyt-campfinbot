import humanize

import campfinbot

def format_candidate(c):
    """
    Returns an object with a single campaign committee and a list
    of associated PACs and SuperPACs, each formatted properly.
    Used for identifying if a given filing should be alerted or not.
    """
    payload = {}
    payload['campaign_committee'] = {"candidate_name": c['name'], "candidate_id": c['candidate_id'], "committee_name": c['name'] + "'s campaign committee", "committee_id": c["committee_id"]}
    payload['associated_committees'] = [{"candidate_name": c['name'], "candidate_id": c['candidate_id'], "committee_name": a['committee']['name'], "committee_id": a['committee']['fecid']} for a in c['associated_committees']]
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
        if filing['fec_committee_id'] in committees:
            if not collection.find_one({'filing_id': filing['filing_id']}):
                if filing['form_type'] in campfinbot.ACCEPTABLE_FORMS:
                    if filing['cash_on_hand']:
                        collection.insert(filing)

                        if alert:
                            message = "*%s* has just filed.\n%s" % (filing['committee_name'], filing['fec_uri'])

                            try:
                                message += "\n\tReceipts: $%s" % humanize.intcomma(round(filing['receipts_total'], 2))
                            except:
                                message += "\n\tReceipts: %s" % filing['receipts_total']

                            try:
                                message += "\n\tCash on hand: $%s" % humanize.intcomma(round(filing['cash_on_hand'], 2))
                            except:
                                message += "\n\tCash on hand: %s" % filing['cash_on_hand']

                            try:
                                message += "\n\tDisbursements: $%s" % humanize.intcomma(round(filing['disbursements_total'], 2))
                            except:
                                message += "\n\tDisbursements: %s" % filing['disbursements_total']

                            messages.append(message)

    return messages