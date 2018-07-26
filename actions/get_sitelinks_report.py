import logging

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

    all_sitelinks = {}
    error_occurred = False

    # To check every sitelink, we need to go through each site in the org
    # and compile a list of all unique sitelinks, then count statuses.
    sites_res = api_auth.site.list_sites()
    if sites_res.status_code != 200:
        return "Failed to get list of sites for getting all sitelinks"

    for site in sites_data.json()["items"]:
        sitelinks_res = api_auth.sitelink.get_sitelinks(site["id"])
        if sitelinks_res.status_code == 404:
            pass # No sitelinks for this site
        elif sitelinks_res.status_code != 200:
            # We'll log an error and skip this one.
            logging.warn("Failed to get sitelinks for {}".format(site["id"]))
            error_occurred = True
        else:
            for sitelink in sitelinks_res.json()["items"]:
                if sitelink["id"] not in all_sitelinks:
                    all_sitelinks[sitelink["id"]] = sitelink

    # Now let us summarise these sitelinks.
    return "There are {} sitelinks".format(len(all_sitelinks))

