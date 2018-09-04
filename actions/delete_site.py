import logging

from flask import json
from actions.util import *

def delete_site(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    
    try:
        site_name = parameters["name"]
        city = parameters["City"]
        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:

        error_string = "Error processing deleteSite intent. {0}".format(e)

        logging.error(error_string)

        return error_string

    # Grab site id by name, city and country
    try:
        site_id = get_site_id_by_name(api_auth, site_name, city, country_code)
    except APIError as e:
        return str(e)

    # Deleting site
    res = api_auth.site.delete_site(site_id)

    if res.status_code == 200:
        speech = "Site {} in {} {} has been successfully deleted".format(site_name, city, country_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not delete site"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech