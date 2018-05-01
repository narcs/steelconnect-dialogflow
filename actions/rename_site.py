import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests

def rename_site(api_auth, parameters):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    
    try:
        old_name = parameters["OldName"]
        new_name = parameters["NewName"]
        city = parameters["City"]

        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:

        error_string = "Error processing createSite intent. {0}".format(e)

        logging.error(error_string)

        return error_string

    # Grabbing list of sites
    res = api_auth.site.list_sites()


    # Grab site id by name, city and country
    if res.status_code == 200:
        data = res.json()["items"]
        site_id = "blank"
        for site in data:
            if site["name"] == old_name and site["city"] == city and site["country"] == country_code:
                    site_id = site["id"]
                    break

        # Renaming site
        res2 = api_auth.site.rename_site(site_id, new_name, new_name, city, country_code)

        if res2.status_code == 200:
            speech = "Site {} has been successfully renamed to {}".format(old_name, new_name)
        elif res2.status_code == 400:
            speech = "Invalid parameters: {}".format(res2.json()["error"]["message"])
        elif res2.status_code == 500:
            speech = "Error: Could not rename site"
        else:
            speech = "Error: Could not connect to SteelConnect"

    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not create site"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    print(speech)
    return speech