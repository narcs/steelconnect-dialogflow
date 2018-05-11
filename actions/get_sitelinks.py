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

    res = api_auth.sitelink.get_sitelinks()

    if res.status_code == 200:
        data = res.json()["items"]
    else:
        speech = "Error: Could not connect to SteelConnect"

    return speech
