import logging
from collections import Counter
from flask import json
from actions.util import *

def get_sitelinks_report(api_auth, parameters, contexts):
    """
    Allows users to get a quick overview in terms of how many sitelinks have which status. That is,
    how many are up, down, established and needs attention. 

    Works by getting getting all the sites, and for each site, we retrieve the associated sitelink
    using get_sitelinks_report.py defined in api/sitelink.py. Once done, we use a Counter to keep
    track of which statuses we have. 
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, it takes
                  on no parameters
    
    Returns:
    - speech: A string which has the health check information about the sitelinks in the organisation

    Example Prompt:
    - sitelinks health check

    """

    all_sitelinks = []
    error_occurred = False

    # To check every sitelink, we need to go through each site in the org
    # and compile a list of all unique sitelinks, then count statuses.
    # I haven't seen a way to just get a list of all sitelinks in an org.
    # FIXME: This often takes too long, and Dialogflow times out. I think
    # the timeout is five seconds.
    sites_res = api_auth.site.list_sites()
    if sites_res.status_code != 200:
        return "Failed to get list of sites for getting all sitelinks"

    for site in sites_res.json()["items"]:
        logging.info("Checking site {}".format(site["id"]))

        sitelinks_res = api_auth.sitelink.get_sitelinks(site["id"])
        if sitelinks_res.status_code == 404:
            pass # No sitelinks for this site
        elif sitelinks_res.status_code != 200:
            # We'll log an error and skip this one.
            logging.warn("Failed to get sitelinks for {}".format(site["id"]))
            error_occurred = True
        else:
            for sitelink in sitelinks_res.json()["items"]:
                logging.info("  Sitelink: {} | {} -> {} | {}".format(sitelink["id"],
                    site["id"], sitelink["remote_site"], sitelink["status"]))
                all_sitelinks.append(sitelink)


    # It seems that sitelinks have different IDs depending on which side
    # you're on. So all sitelinks are counted twice.
    # I will assume both sides have the same state. This may be technically
    # incorrect though.

    # Now let us summarise these sitelinks.
    # Because I don't know all the statuses, I'm just going to count what I see.
    statuses = Counter()

    for sitelink in all_sitelinks:
        statuses[sitelink["state"]] += 1

    n_sitelinks = len(all_sitelinks) / 2
    if n_sitelinks == 1:
        speech = "There is 1 sitelink"
    else:
        speech = "There are {} sitelinks".format(len(all_sitelinks) / 2)

    for status in statuses:
        speech += "\n  - {} {}".format(statuses[status] / 2, status)

    return speech

