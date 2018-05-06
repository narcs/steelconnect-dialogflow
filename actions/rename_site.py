import logging

from flask import json
from actions.util import *

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

    # Grab site id by name, city and country
    try:
        site_id = get_site_id_by_name(api_auth, old_name, city, country_code)
    except APIError as e:
        return str(e)

    # Renaming site
    res = api_auth.site.rename_site(site_id, new_name, new_name, city, country_code)

    if res.status_code == 200:
        speech = "Site {} in {} {} has been successfully renamed to {}".format(old_name, city, country_name, new_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not rename site"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    print(speech)
    return speech