import logging
from flask import json

def get_uplink_info_followup(api_auth, parameters, contexts):
    try: 
        option_choice = int(parameters["OptionNumber"])
    except KeyError as e:
        error_string = "Error processing getting uplink information followup"
        logging.error(error_string)
        return error_string

    uplinks_res = api_auth.uplink.get_uplink_info()
    if uplinks_res.status_code != 200:
        return "Failed to get a list of uplinks"
    
    uplinks = uplinks_res.json()["items"]
    uplink_information = uplinks[option_choice - 1]
    information = api_auth.uplink.format_uplink_information(uplink_information)
    speech = "Information for Uplink {}: \n{}".format(uplink_information["id"], information)

    return speech