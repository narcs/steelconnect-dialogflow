import logging

from flask import json

def create_wan(api_auth, parameters, contexts):
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
        WAN_type = parameters["WANType"]
        name = WAN_type

    except KeyError as e:

        error_string = "Error processing createWAN intent. {0}".format(e)

        logging.error(error_string)

        return error_string

    res = api_auth.create_wan(name)

    if res.status_code == 200:
        speech = "{} created".format(WAN_type)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not create WAN"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

