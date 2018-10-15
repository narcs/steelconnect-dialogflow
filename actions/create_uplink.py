import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests
from util import get_site_id_by_name, APIError


def create_uplink(api_auth, parameters, contexts):
    """
    Allows users to create an uplink from a particular site to a WAN. 
    In order for them to do so, we need to know the city, site name, country code, uplink name and
    WAN to connect to 

    Works by checking if the site exists. If it exists, it will then proceed to check if the WAN 
    type specified matches what the user inputs. If it does, it calls the SteelConnectAPI and 
    creates the uplink 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > site_name: the name of the site the user wants to connect the uplink
        > uplink_name: the name of the uplink the user wants to give to the uplink
        > wan_name: the name of the wan te user wants to connect the site to
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Create an uplink called Arbok from the ekans site in kiev, ukraine to VPN

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

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be created on
    data_wans = api_auth.wan.list_wans().json()
    wan = " "
    for item in data_wans["items"]:
        if wan_name == item["name"]:
            wan = item["id"]
            break
    else:           #If it doesn't match, print user friendly message
        speech = "Unfortunately the WAN {} does not exist. Please select a different WAN that the uplink could connect to".format(wan_name)
        return speech    

    # call create uplink api
    res = api_auth.uplink.create_uplink(site_id, uplink_name, wan)

    if res.status_code == 200:
        speech = "An uplink called {} has been created between the {} site and the {} WAN ".format(uplink_name, site_name, wan_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not create uplink"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    return speech
