import logging

from flask import json
from actions.util import get_wan_id_by_name, APIError

def delete_wan(api_auth, parameters, contexts):
    """
    Allows users to delete a WAN 
    In order for them to do so, we need to know the WAN name

    Works by getting the name of the WAN the user wants to delete, getting it's associated id, 
    and deleting the WAN based of the id.

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > WAN_Name: The name of the WAN the user wants to delete

    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Delete the WAN named LTE

    """
    WAN_Name = parameters["WANName"]
    wan_id = None

    logging.debug("Attempting to delete WAN named: " + WAN_Name)

    try:
        wan_id = get_wan_id_by_name(api_auth, WAN_Name)
    except APIError as e:
        return str(e)

    # Now delete the WAN!
    res = api_auth.wan.delete_wan(wan_id)
    if res.status_code == 200:
        speech = "The {} WAN has successfully been deleted".format(WAN_Name)
    elif res.status_code == 500:
        # Deletion failed.
        speech = "The {} WAN could not be deleted.".format(WAN_Name)
    else:
        speech = "Error: Other error while attempting to delete the WAN"

    logging.debug(speech)

    return speech

