import logging
from flask import json

def list_uplinks(api_auth, parameters, contexts):
    """
    Allows users to list all the uplinks that are in the organisation and get a brief overview
    in terms of which site and WAN it is connected to and the name of the uplink

    Works by calling the list_uplinks action defined in api/uplink.py

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, we
                  obtain nothing

    Returns:
    - speech: A string which has the list of all uplinks in the organisation

    Example Prompt:
    - List uplinks

    """
    
    # Get all uplinks and return a response based on the number of uplinks
    res = api_auth.uplink.list_uplinks()

    if res.status_code == 200:
        data = res.json()["items"]
        num_uplinks = len(data)

        if num_uplinks == 0:
            speech = "There are no uplinks"
        elif num_uplinks >= 1:
            speech = "There are {} uplinks in the organisation:\n".format(num_uplinks)
            count = 1
            for uplink in data:
                site = api_auth.site.get_site(uplink["site"])
                site_name = site.json()["longname"]
                name = uplink["name"]
                wan = api_auth.wan.get_wan(uplink["wan"])
                wan_name = wan.json()["longname"]

                #added leading zeroes in the count variable to help with formatting of data
                speech += "\n{}. ID: {}\n\t  Site: {}\n\t  Uplink Name: {}\n\t  Connected WAN: {}\n".format(str(count).zfill(len(str(num_uplinks))), uplink["id"], site_name, name, wan_name)
                count += 1
        else:
            speech = "Unknown error occurred when retrieving uplinks"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    return speech