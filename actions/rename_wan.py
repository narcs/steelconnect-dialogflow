import logging

from flask import json
from actions.util import *

def rename_wan(api_auth, parameters, contexts):
    """
    Changes the short name of a WAN.

    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :param contexts: json contexts from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    original_name = parameters["OriginalName"]
    new_name = parameters["NewName"]

    try:
        wan_id = get_wan_id_by_name(api_auth, original_name)
    except APIError as e:
        return str(e)

    new_data = {
        "name": new_name,
        "longname": new_name
    }
    res = api_auth.update_wan(wan_id, new_data)

    if res.status_code == 200:
        speech = "Renamed '{}' to '{}'".format(original_name, new_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not rename WAN"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

