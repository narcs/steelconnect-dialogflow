import logging

from flask import json
from actions.util import *

def get_wan(api_auth, parameters, contexts):
    """
    Gets details about a specific WAN.

    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :param contexts: json contexts from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    wan_name = parameters["WANName"]
    wan_id = None

    try:
        wan_id = get_wan_id_by_name(api_auth, wan_name)
    except APIError as e:
        return str(e)

    res = api_auth.wan.get_wan(wan_id)
    data = res.json()

    if res.status_code == 200:
        template = """Name: {}
Long name: {}
REST API ID: {}
No. of uplinks connected to this WAN: {}"""

        speech = template.format(data["name"], data["longname"] if data["longname"] is not None else "<none>", wan_id, len(data["uplinks"]))
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not get WAN details"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

