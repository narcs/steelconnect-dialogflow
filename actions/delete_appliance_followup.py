import logging
from flask import json

def delete_appliance_followup(api_auth, parameters, contexts):
    """
    Allows users to delete a specific appliance on a site, in cases where there are multiple
    appliances of the same model. In order to do this, we only retrieve a single option number.
    It is done this way because the unique identifier is a very long string and we do not 
    expect users to be able to remember the identifier. Hence, option numbers are currently the 
    best way to go. 

    Works by retrieving the list of appliances that match the model and site that the user requests
    to delete. It asks the user for an option number, and delete the appliance that matches the 
    option number the user put in. 

    We do not need to check if the site exists because this has already been done in
    delete_appliance.py 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > option_choice: An integer that references an option to delete the appliance
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - 1

    """
    try:
        option_choice = int(parameters["OptionNumber"])
    except KeyError as e:
        error_string = "Error processing deleting appliance followup"
        logging.error(error_string)
        return error_string
    
    appliance_options = api_auth.node.get_appliance_list()
    appliance_id = appliance_options[option_choice - 1]         #option_choice - 1 because arrays start at zero, so whatever the user inputs, we just need to subtract 1 from it
    res = api_auth.node.delete_appliance(appliance_id)
    if res.status_code == 200:
        speech = "Successfully deleted appliance {}".format(appliance_id)
    else:
        speech = "Appliance {} could not be deleted".format(appliance_id)
    return speech