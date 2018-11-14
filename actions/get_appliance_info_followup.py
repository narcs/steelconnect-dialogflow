import logging
from flask import json

def get_appliance_info_followup(api_auth, parameters, contexts):
    """
    Allows users to get detailed information about a particular appliance,in cases where there are 
    multiple appliances of the same model. In order to do this, we only retrieve a single option 
    number. It is done this way because the unique identifier is a very long string and we do not 
    expect users to be able to remember the identifier. Hence, option numbers are currently the 
    best way to go. 

    Works by retrieving the list of appliances that match the model and site that the user requests
    to get detailed information about. It asks the user for an option number, and delete the 
    appliance that matches the option number the user put in. A check is done to make sure it is 
    within range

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > option_choice: An integer that references an option to delete the appliance

    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - 2

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
        if option_choice < 1 or option_choice > len(appliance_options):        #Check to see if the value the user inputted is within range
            speech = "Please selected a number between 1 and {}".format(len(appliance_options))
        else:
            appliance_info = res.json()
            information = api_auth.node.format_appliance_information(appliance_info)
            speech = "Information for Appliance ID: {}\n{}".format(appliance_id, "".join(information))
    else:
        return "Error: Failed to get information for Appliance {}".format(appliance_id)
    return speech    