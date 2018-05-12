import logging
from flask import json
from requests.auth import HTTPBasicAuth
import requests
from util import get_site_id_by_name, APIError

def create_appliance(api_auth, parameters, contexts):
    """
    Allows users to create an appliance on a site. 
    In order for them to do so, we need to know the city, site name
    model and country code. 

    :param api_auth: SteelConnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        city = parameters["City"].replace(" ", "")  # .replace() is for locations where there are spaces. E.g. Kuala Lumpur
        site_name = parameters["SiteName"]
        model = parameters["Model"]
        country_code = parameters["Country"]["alpha-2"]
 
    except KeyError as e:
        error_string = "Error processing create Appliance intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all sites and check whether site exists
    # Currently, if site doesn't exist it just says not available
    # Need to fix it, but depends on how get_site_id_by_name is implemented 
    try:
        site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    except APIError as E:
        return str(E)    

    data_sites = api_auth.site.list_sites().json()
    for item in data_sites["items"]:
        if item["id"] == site_id:
            break

    if site_id:
        # Call create_appliance in SteelConnectAPI
        res = api_auth.node.create_appliance(site=site_id, model=model)
 
        if res.status_code == 200:
            speech = "Appliance: {} created for site: {}, {}".format(model, city, site_name)
        elif res.status_code == 400:
            speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
        elif res.status_code == 404:
            speech = "Error: Organization with given id does not exist"
        elif res.status_code == 500:
            speech = "Error: Could not create Appliance"
        else:
            speech = "Error: Could not connect to SteelConnect"
 
        logging.debug(speech)
    else:
        speech = "Invalid site {} in {}".format(site_name, city)
    return speech

