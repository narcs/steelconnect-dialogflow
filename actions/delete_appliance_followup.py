import logging
from flask import json

def delete_appliance_followup(api_auth, parameters, contexts):
    """
    A follow up for when users want to delete an appliance on a site
    Because the only unique identifier is a very long strong, it is
    tedious for user to enter it. This gives them option numbers to 
    choose from.  

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