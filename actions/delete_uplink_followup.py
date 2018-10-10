import logging

from flask import json

def delete_uplink_followup(api_auth, parameters, contexts):
    """
    Allows users to delete a specific uplink, in cases where there are multiple uplinks connecting
    the same site to the same WAN. In order to do this, we only retrieve a single option number.
    It is done this way because the unique identifier (which is a very long string) is the only way 
    to differentiate between the uplinks that connect the same WAN and site. We do not expect users 
    to be able to remember the identifier. Hence, option numbers are currently the best way to go. 

    Works by retrieving the list of uplinks that match the WAN and site that the user requests
    to delete. It asks the user for an option number, and checks to see if it is within the range.
    If it is, it will delete the uplink that matches the option number the user put in. 

    We do not need to check if the site and WAN exists because this has already been done in
    delete_uplink.py 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > option_choice: An integer that references an option to delete the uplink
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - 1

    """
    try:
        option_choice = int(parameters["OptionNumber"])
    except KeyError as e:
        error_string = "Error processing delete uplink follow up. {0}".format(e)
        logging.error(error_string)
        return error_string

    #don't need to check status code because we are not calling any APIs
    uplink_options = api_auth.uplink.get_uplink_list()

    if option_choice < 1 or option_choice > len(uplink_options):        #Check to see if the value the user inputted is within range
        speech = "Please selected a number between 1 and {}".format(len(uplink_options))
    else:       #If it is within the given value, then delete the associated uplink
        uplink_id = uplink_options[option_choice - 1]         #option_choice - 1 because arrays start at zero, so whatever the user inputs, we just need to subtract 1 from it
        res = api_auth.uplink.delete_uplink(uplink_id)
        if res.status_code == 200:
            speech = "Successfully deleted uplink {}".format(uplink_id)
        else:
            speech = "uplink {} could not be deleted".format(uplink_id)
    return speech