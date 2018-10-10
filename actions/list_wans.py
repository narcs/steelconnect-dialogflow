import logging
from flask import json
from actions.util import *

def list_wans(api_auth, parameters, contexts):
    """
    Allows users to list all the WANs that are in the organisation

    Works by calling the list_WANs action defined in api/wans.py

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, we
                  obtain nothing

    Returns:
    - speech: A string which has the list of all WANs in the organisation

    Example Prompt:
    - List WANs

    """

    logging.info("Listing WANs")

    res = api_auth.wan.list_wans()
    if res.status_code == 200:
        data = res.json()["items"]
        num_WANs = len(data)

        if num_WANs == 0:
            speech = "There are no WANs"
        elif num_WANs >= 1:
            speech = "There are {} WANs in the organisation:\n".format(num_WANs)
            count = 1

            for WAN in data:
                name = WAN["longname"]
                id = WAN["id"]
                num_uplinks_attached = len(WAN["uplinks"])
                speech += "\n{}. ID: {}\n\t  WAN: {}\n\t  Number Of Uplinks Attached: {}\n".format(str(count).zfill(len(str(num_WANs))), id, name, num_uplinks_attached)                
                count += 1
        else:
            speech = "Unknown error occurred when retrieving WANs"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    return speech