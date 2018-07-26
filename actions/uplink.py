import logging

from flask import json

def list_uplinks(api_auth, parameters, contexts):
    """
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    
    # Get all uplinks and return a response based on the number of uplinks
    res = api_auth.uplink.list_uplinks()

    if res.status_code == 200:
        data = res.json()["items"]
        num_uplinks = len(data)

        if num_uplinks == 0:
            speech = "There are no uplinks"
        elif num_uplinks >= 1:
            speech = "All uplinks:\n"
            count = 1
            for uplink in data:
                site = api_auth.site.get_site(uplink["site"])
                site_name = site.json()["longname"]
                name = uplink["name"]
                wan = api_auth.wan.get_wan(uplink["wan"])
                wan_name = wan.json()["longname"]

                speech += "\n {}. {}/{}/{}".format(count, site_name, name, wan_name)
                count += 1

        else:
            speech = "Unknown error occurred when retrieving uplinks"

    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech