import logging
import requests
from flask import json
from requests.auth import HTTPBasicAuth
from util import get_site_id_by_name, APIError

def get_uplink_info (api_auth, parameters, contexts):
    """
    Allows users to get detailed information about a particular uplink that connects a particular
    site to a particular WAN. 

    Works by checking if the site exists. If it exists, it then checks to see if the specified WAN
    exists. If it doesn't the user will be prompted, and no uplink information will be retrieved.If
    it does exist, it will get all the uplink information, and will try to find the uplinks that 
    matches the uplink name, site name and WAN. If there is only one, it will display the 
    information to the user. If there are multiple, they will be redirected to
    get_uplink_info_followup.py to specify which one they want, using a terminal-like interface. If
    there aren't any, they will be informed. It is done this way because there is no other way to
    uniquely distinguish between the uplinks apart from the ID (which is very long and difficult to
    remember) when the site name, WAN and uplink name are all the same. 
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > wan_name: The name of the WAN the user wants to delete the connecting uplink from
        > site_name: the name of the site the user wants to remove the uplink from
        > uplink_name: the name of the uplink the user wants to delete
    
    Returns:
    - speech: A string which has the list of all uplinks in the organisation that matches the user specification

    Example Prompt:
    - Get information on the goldeen uplink connecting the seaking site in London, Britain to the RouteVPN WAN

    """
    try:
        site_name = parameters["SiteName"]
        uplink_name = parameters["UplinkName"]
        wan_name = parameters["WANName"]
        city = parameters["City"]
        country_code = parameters["Country"]["alpha-2"]
        
    except KeyError as e:
        error_string = "Error processing createUplink intent. {0}".format(e)
        logging.error(error_string)
        return error_string
		
    try:
        site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    except APIError as E:
        return str(E) 

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be deleted
    data_wans = api_auth.wan.list_wans().json()
    for item in data_wans["items"]:
        if wan_name == item["name"]:        #if we have a wan name that matches, we can break and continue on
            break
    else:           #If it doesn't match, print user friendly message
        speech = "Unfortunately the WAN {} does not exist. Please select a different WAN that the uplink may be connected to".format(wan_name)
        return speech  

    uplink_list = api_auth.uplink.get_uplink_info()         #Get all the uplink information
    if uplink_list.status_code == 200:
        data = uplink_list.json()["items"]
        connected_uplinks = []
        for uplink in data:
            if uplink["site"] == site_id and uplink_name == uplink["name"]:     #if it matches the specified site and uplink, then hold onto that information
                connected_uplinks.append(uplink)
    else:
        return "Error: Failed to get relevant uplinks"

    if len(connected_uplinks) == 1:         #If we only have one uplink that matches the specifications, then display the information
        uplink_information = connected_uplinks[0]
        information = api_auth.uplink.format_uplink_information(uplink_information)
        speech = "Information for the {} uplink connecting the {} site to the {} WAN: \n{}".format(uplink_name, site_name, wan_name, "".join(information))
    elif len(connected_uplinks) > 1:        #If there are multiple, prompt the user for a specific one using terminal style
        uplink_options = []
        count = 1
        uplink_options_response = "\n"
        for uplink in connected_uplinks:
            uplink_options_response += "Option " + str(count) + ": " + str(uplink["id"]) + "\n"     #prepare the prompt statement
            uplink_options.append(uplink)
            count += 1
        api_auth.uplink.set_uplink_list(uplink_options)
        speech = "There are multiple {} uplinks connecting the {} site to the {} WAN. Please choose a value from the following:\n {}".format(uplink_name, site_name, wan_name, uplink_options_response)
    else:
        speech = "There were no {} uplinks connecting the {} site to the {} WAN. Please try a different uplink name, site or WAN.".format(uplink_name, site_name, wan_name)
    return speech