
import campfinbot
from campfinbot import utils

outputs = []
crontable = []
crontable.append([86400, "summarize_f24s"])


def summarize_f24s():
    """
    alerts all f24's that have not yet been alerted
    """
    f24s = campfinbot.MONGODB_DATABASE.presidential_filings.find({'form_type':'F24', 'alerted':None})

    message = ""
    for f in f24s:
        if 'alerted' in f and f['alerted']: #should only have loaded non-alerted, but double checking
            continue
        if f['filed_date'] <= campfinbot.EARLIEST_ALERT:
            continue
        info = {'comm':f['committee_name'],
                'ie_count':f['num_ies'],
                'link':f['source_url'],
                'date':f['filed_date']
                }
        message += "\n\t [{date}] {comm} filed an F24 with {ie_count} IEs: {link}".format(**info)
        f['alerted'] = True
        campfinbot.MONGODB_DATABASE.presidential_filings.save(f)

    if message:
        message = "New F24's (since last alert):" + message

        outputs.append([campfinbot.CHANNEL,message])
