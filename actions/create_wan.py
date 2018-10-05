import logging
from flask import json

def create_wan(api_auth, parameters, contexts):
    """
    Allows users to create a WAN 
    In order for them to do so, we need to know the WAN type and a name for the WAN

    Works by getting the parameters, and calling the SteelConnect API with the parameters to create
    the WAN

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > WAN_Name: A name/label the user gives for the WAN they create

    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Create a WAN named FireStone

    """
    try:
        WAN_Name = parameters["WANType"]       

    except KeyError as e:
        error_string = "Error processing createWAN intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    res = api_auth.wan.create_wan(WAN_Name)         #Calls SteelConnectAPI and creates the WAN

    if res.status_code == 200:
        speech = "A WAN called {} was created".format(WAN_Name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not create WAN {}".format(WAN_Name)
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

