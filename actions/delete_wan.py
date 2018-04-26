import logging

from flask import json
from actions.util import *

def delete_wan(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    wan_name = parameters["WANName"]
    wan_id = None

    logging.debug("Attempting to delete WAN named: " + wan_name)

    try:
        wan_id = get_wan_id_by_name(api_auth, wan_name)
    except APIError as e:
        return str(e)

    # Now delete the WAN!
    res = api_auth.delete_wan(wan_id)
    if res.status_code == 200:
        speech = "Successfully deleted the WAN named '{}'".format(wan_name)
    elif res.status_code == 500:
        # Deletion failed.
        speech = "The WAN could not be deleted."
    else:
        speech = "Error: Other error while attempting to delete the WAN"


    logging.debug(speech)

    return speech

