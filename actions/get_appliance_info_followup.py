import logging
from flask import json

def get_appliance_info_followup(api_auth, parameters, contexts):
    """
    A follow up for when users want to get information about a 
    specific appliance. Because the only unique identifier is a 
    very long strong, it is tedious for user to enter it. 
    This gives them option numbers to choose from.  

    :param api_auth: SteelConnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        option_choice = int(parameters["OptionNumber"])
    except KeyError as e:
        error_string = "Error processing getting appliance information follow up intent"
        logging.error(error_string)
        return error_string
    
    appliance_options = api_auth.node.get_appliance_list()
    appliance_id = appliance_options[option_choice - 1]     #option_choice -1 because arrays start at zero <-- this is more of a reminder sort of thing...
    res = api_auth.node.get_appliance_info(node_id= appliance_id)
    if res.status_code == 200:
        appliance_info = res.json()
        information = api_auth.node.format_appliance_information(appliance_info)
        speech = "Information for Appliance ID: {}\n{}".format(appliance_id, "".join(information))
    else:
        return "Error: Failed to get information for Appliance {}".format(appliance_id)
    return speech    