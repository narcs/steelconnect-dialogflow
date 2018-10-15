import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def create_site(api_auth, parameters, contexts):
    """
    Allows users to create a site 
    In order for them to do so, we need to know the city, site name and country code. 

    Works by getting the parameters, and calling the SteelConnect API with the parameters to create
    the site

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: The city where the user wants to create the site
        > country_code: The country code of where the user wants to create the site
            + The country name will be obtained from the country code, and will not be directly
              retrieved from the user
        > site_name: A name that the user gives the site they want to create 
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - create a site called bulbasaur in Hobart, Australia

    """
    try:
        site_name = parameters["SiteName"]
        city = parameters["City"]

        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:
        error_string = "Error processing createSite intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    res = api_auth.site.create_site(site_name, city, country_code)          #Creates the site 

    if res.status_code == 200:
        speech = "A site named {} has been created in {}, {}".format(site_name, city, country_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: We could not create the {} site at {}, {}".format(site_name, city, country_name)
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech

