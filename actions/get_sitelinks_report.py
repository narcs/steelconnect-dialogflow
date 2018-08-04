import logging
from collections import Counter

from flask import json
from actions.util import *

def get_sitelinks_report(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """


    all_sitelinks = []
    error_occurred = False

    # To check every sitelink, we need to go through each site in the org
    # and compile a list of all unique sitelinks, then count statuses.
    # I haven't seen a way to just get a list of all sitelinks in an org.
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

