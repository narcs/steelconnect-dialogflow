import logging
from flask import json
from actions.util import *

def get_wan(api_auth, parameters, contexts):
    """
    Allows users to get detailed information about a particular WAN

    Works by checking if the WAN exists. If it exists, it gets the information about the WAN via 
    the get_wan() method. It then extracts and formats the data

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > WAN_name: the name of the WAN the user wants to retreive information about

    Returns:
    - speech: A string which has the health check information about the WANs in the organisation

    Example Prompt:
    - Get details of the WAN named GlobalNet

    """

    WAN_name = parameters["WANName"]
    WAN_id = None

    try:
        WAN_id = get_wan_id_by_name(api_auth, WAN_name)
    except APIError as e:
        return str(e)

    res = api_auth.wan.get_wan(WAN_id)
    data = res.json()

    if res.status_code == 200:
        template = """*WAN ID:* {}\n*Name:* {}\n*Organisation:* {}\n*Trusted:* {}\n*Internet:* {}\n*Internet Nat:* {}\n*DCuplink:* {}\n*pingcheck_profile:* {}\n*pingcheck_ips:* {}\n*ping_gw:* {}\n*Encryption:* {}\n*uid:* {}\n*Sitelink:* {}\n*Number Of Connected Uplinks:* {}\n*Connected Uplinks:* \n\t{}\n"""
        speech = template.format(WAN_id, data["name"], data["org"], data["trusted"], data["internet"], data["Internet_NAT"], data["dcuplink"] , data["pingcheck_profile"] , data["pingcheck_ips"], data["ping_gw"] , data["encryption"] , data["uid"], data["sitelink"], len(data["uplinks"]), "\n\t".join(data["uplinks"]))
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not get WAN details"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

