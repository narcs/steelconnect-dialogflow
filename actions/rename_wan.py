import logging
from flask import json
from actions.util import *

def rename_wan(api_auth, parameters, contexts):
    """
    Allows users to rename an existing site

    Works by getting the WAN id from the WAN name. From there it changes the
    old WAN name to the new WAN name using the update_wan method defined in api/WAN
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > original_name: the name of the WAN the user wants to change
        > new_name: the new name of the WAN the user wants to give
    
    Returns:
    - speech: A string which lets the user know if the WAN has been renamed or not

    Example Prompt:
    - Rename the WAN named WAN to GlobalNet

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
    res = api_auth.wan.update_wan(wan_id, new_data)

    if res.status_code == 200:
        speech = "Renamed the {} WAN to {}".format(original_name, new_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not rename WAN"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

