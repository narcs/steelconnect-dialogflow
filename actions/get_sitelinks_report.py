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

    # To check every sitelink, we need to go through each site in the org
    # and compile a list of all unique sitelinks, then count statuses.



    res = api_auth.sitelink.get_sitelinks(site_id)
    speech = ""

    if res.status_code == 200:
        data = res.json()["items"]
        if len(data) != 0:
            speech = "Tunnels from {}: {}".format(site_name, format_sitelink_list(api_auth, data))

    elif res.status_code == 404:
        speech = "There are no tunnels from {}".format(site_name)
    else:
        speech = "Error: Unspecified error"

    return speech
