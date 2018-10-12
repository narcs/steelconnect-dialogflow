import logging
from flask import json

def get_uplink_info_followup(api_auth, parameters, contexts):
    """
    Allows users to get information about a specific uplink, in cases where there are multiple 
    uplinks connecting the same site to the same WAN. In order to do this, we only retrieve a single
    option number. It is done this way because the unique identifier (which is a very long string) 
    is the only way to differentiate between the uplinks that connect the same WAN and site. We do 
    not expect users to be able to remember the identifier. Hence, option numbers are currently the 
    best way to go. 

    Works by checking if the inputted number is within a valid range. If it is, it will retrieve 
    the uplink information associated with the option number in the list of uplink information 
    collected in get_uplink_info.py. We do not need to check if it matches the specified WAN and 
    site as this is already done in get_uplink_info.py. 
    
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
        error_string = "Error processing getting uplink information followup"
        logging.error(error_string)
        return error_string

    uplink = api_auth.uplink.get_uplink_list()

    #Don't need to check status code because we are not calling any APIs
    if option_choice < 1 or option_choice > len(uplink):        #Check to see if the value the user inputted is within range
        speech = "Please selected a number between 1 and {}".format(len(uplink))
    else:       #If it is within the given value, then delete the associated uplink
        uplink_information = uplink[option_choice - 1]
        information = api_auth.uplink.format_uplink_information(uplink_information)
        speech = "Information for Uplink {}: \n{}".format(uplink_information["id"], "".join(information))
    return speech