import logging

from flask import json
from actions.util import *

def get_sitelinks(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    site_name = parameters["SiteName"]
    site_city = parameters["SiteCity"]
    site_country_id = parameters["SiteCountry"]["alpha-2"]
    site_id = ""

    try:
        site_id = get_site_id_by_name(api_auth, site_name, site_city, site_country_id)
    except APIError as e:
        return str(e)

    res = api_auth.sitelink.get_sitelinks(site_id)
    speech = ""

    if res.status_code == 200:
        data = res.json()["items"]
        if len(data) != 0:
            speech = "Tunnels from {}: {}".format(site_name, format_sitelink_list(api_auth, data))
        else:
            speech = "There are no tunnels from {}".format(site_name)

    else:
        speech = "Error: Could not connect to SteelConnect"

    return speech
