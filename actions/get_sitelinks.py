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

    # TODO: Get site ID from name.
    res = api_auth.sitelink.get_sitelinks("site-HQ-5e84559c484455da")
    speech = ""

    if res.status_code == 200:
        data = res.json()["items"]
        speech = "Tunnels from {}: {}".format("<site-name>", format_sitelink_list(data))

    else:
        speech = "Error: Could not connect to SteelConnect"

    return speech
