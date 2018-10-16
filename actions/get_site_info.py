import logging

from flask import json
from actions.util import *

def get_site_info(api_auth, parameters, contexts):
    """
    Allows users to get detailed information about a particular SITE

    Works by checking if the SITE exists. If it exists, it gets the information about the SITE via 
    the get_site() method. It then extracts and formats the data

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > name: the name of the site the user wants to retreive information about
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        
    Returns:
    - speech: A string which has the health check information about a site in the organisation

    Example Prompt:
    - Get details of the site Branch in Sydney Australia
    """
    
    try:
        name = parameters["Name"]
        city = parameters["City"]

        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:

        error_string = "Error processing getSiteInfo intent. {0}".format(e)

        logging.error(error_string)

        return error_string

    # Grab site id by name, city and country
    try:
        site_id = get_site_id_by_name(api_auth, name, city, country_code)
    except APIError as e:
        return str(e)

    # Getting site info
    res = api_auth.site.get_site(site_id)

    if res.status_code == 200:
        information = api_auth.site.format_site_info(res.json())
        # Appending list of uplinks
        information.append("*Uplinks:* {}".format("\n\t".join(res.json()["uplinks"])))
        speech = "*Information for site {}:* \n{}".format(name, information)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not get site information"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech