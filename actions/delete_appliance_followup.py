import logging
from flask import json

def delete_appliance_followup(api_auth, parameters, contexts):
    try:
        option_choice = int(parameters["OptionNumber"])
    except KeyError as e:
        error_string = "Error processing deleteing appliance followup"
        logging.error(error_string)
        return error_string
    
    appliance_options = api_auth.node.get_appliance_list()
    appliance_id = appliance_options[option_choice - 1]
    res = api_auth.node.delete_appliance(appliance_id)
    if res.status_code == 200:
        speech = "Successfully deleted appliance {}".format(appliance_id)
    else:
        speech = "Appliance {} could not be deleted".format(appliance_id)
    return speech