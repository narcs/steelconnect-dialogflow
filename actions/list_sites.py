import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests

def list_sites(api_auth, parameters, contexts):
    """
    Allows users to list all the sites that are in the organisation and where they are 
    located

    Works by calling the list_sites action defined in api/site.py

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, we
                  obtain nothing

    Returns:
    - speech: A string which has the list of all sites in the organisation

    Example Prompt:
    - List sites

    """
    # Get org name from Entitities
    org = parameters["organisation"]

    # Get all sites and return a response based on the number of sites
    res = api_auth.site.list_sites()

    if res.status_code == 200:
        data = res.json()["items"]
        num_sites = len(data)
        
        if num_sites == 0:
            speech = "There are no sites in the {} organisation".format(org)
        elif num_sites == 1:
            speech = "There is one site in the {} organisation, it is called {}".format(org, data[0]["name"])
        elif num_sites > 1:
            speech = "There are {} sites in the organisation: \n".format(num_sites)
            count = 1
            for site in data:
                name = site["name"]
                city = site["city"]
                country = site["country"]
                site_id = site["id"]
                
                #added leading zeroes in the count variable to help with formatting of data
                speech += "\n{}. ID: {}\n\t  Site Name: {}\n\t  City: {}\n\t  Country: {}\n".format(str(count).zfill(2), site_id, name, city, country)
                count += 1
        else:
            speech = "Unknown error occurred when retrieving sites"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    return speech
