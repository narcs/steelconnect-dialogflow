import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests

def list_sites(api_auth, parameters):
    """
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
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
            speech = "There are {} sites in the {} organisation: \n".format(
                num_sites, org)
            for site in data:
                name = site["name"]
                city = site["city"]
                country = site["country"]
                speech += "{} in {} {}, \n".format(name, city, country)

            speech = speech[2:] + "."
            
        else:
            speech = "Unknown error occurred when retrieving sites"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech