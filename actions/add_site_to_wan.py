"""
This has not yet been tested or modified since 2017. 
This is potentially deprecated
"""

import logging
from flask import json
from actions import create_uplink
from api.util import find_context_by_name, find_contexts_by_name

def add_site_to_wan(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :param contexts: json contexts from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        wan_context = find_context_by_name(contexts, "wan_created")["parameters"]
        site_context = find_context_by_name(contexts, "sitecreated")["parameters"]

        new_parameters = {"SiteTypes": site_context["SiteType"],
                          "City": site_context["City"],
                          "Wans": wan_context["WANType"],
                          "Uplinks": ""}


    except KeyError as e:

        error_string = "Error processing addSitesToWAN intent. {0}".format(e)

        logging.error(error_string)

        return "Unable to add site to WAN"

    speech = create_uplink.create_uplink(api_auth, new_parameters)

    logging.debug(speech)

    return speech

