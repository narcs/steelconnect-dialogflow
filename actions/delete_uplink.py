import logging
from flask import json
from util import get_site_id_by_name, APIError


def delete_uplink(api_auth, parameters, contexts):
    """
    Allows users to delete an uplink connecting a site to a wan. 
    In order for them to do so, we need to know the city, site name, uplink name, WAN name and 
    country code. 

    Works by checking if the site exists. If it exists, it then checks to see if the WAN exists. If
    it exists, it finds out how many uplinks with the same name that connects the same site and WAN.
    If there is only one, it deletes it. If there are more, then it gets stored in a list, and the 
    user will be prompted to enter a number to delete the appropriate uplink (This is in the 
    delete_uplink_followup.py file.) 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > wan_name: The name of the WAN the user wants to delete the connecting uplink from
        > site_name: the name of the site the user wants to remove the uplink from
        > uplink_name: the name of the uplink the user wants to delete
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Delete the sandslash uplink connecting the toast site in Melbourne , Australia to RouteVPN

    """
    try:
        site_name = parameters["SiteName"]
        uplink_name = parameters["UplinkName"]
        wan_name = parameters["WANName"]
        city = parameters["City"]
        country_code = parameters["Country"]["alpha-2"]

    except KeyError as e:
        error_string = "Error processing deleteUplink intent. {0}".format(e)
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

    data_uplinks = api_auth.uplink.list_uplinks().json()
    uplinks = []
    for uplink in data_uplinks["items"]:
        if ((site_id == uplink["site"]) and (uplink_name == uplink["name"])):
            uplinks.append(uplink["id"])

    if len(uplinks) == 0:
        speech = "Unforunately there were no {} uplinks connecting the {} site to the {} WAN. No uplinks were deleted".format(uplink_name, site_name, wan_name) 
    elif len(uplinks) == 1:
        res = api_auth.uplink.delete_uplink(uplinks[0])
        if res.status_code == 200:
            speech = "The {} uplink connecting the {} site to the {} WAN has now been deleted".format(uplink_name, site_name, wan_name)
        else:
            speech = "Error: Could not connect to SteelConnect"
    elif len(uplinks) > 1:
        uplink_options_response = '\n'
        uplink_options = []
        count = 1
        for u in uplinks:
            uplink_options_response += "Option " + str(count) + ": " + u + "\n"
            uplink_options.append(u)
            count = count + 1
        api_auth.uplink.set_uplink_list(uplink_options)
        speech = "There are multiple {} uplinks connecting the {} site to the {} WAN. Please choose a number from the following: {}".format(uplink_name, site_name, wan_name, uplink_options_response)
    else:
        speech = "Error: There was another error while attempting to delete the uplink"

    logging.debug(speech)
    return speech
