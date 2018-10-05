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

    Works by checking if the site exists. If it exists, it gets the parameters, and with the 
    parameters, it calls the SteelConnectAPI, and creates the appliance 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > model: The model of the appliance the user wants to create
        > site_name: the name of the site the user wants to place the appliance on
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Make an ewok appliance for charmeleon, in Darwin, Australia

    """
    try:
        city = parameters["City"]
        site_name = parameters["SiteName"]
        model = parameters["Model"]
        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
 
    except KeyError as e:
        error_string = "Error processing create Appliance intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all sites and check whether site exists
    # Currently, if site doesn't exist it will let the user know that the site doesn't exist
    try:
        site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    except APIError as E:
        return str(E)    

    if site_id:         #If we find a site that exists
        # Call create_appliance in SteelConnectAPI
        res = api_auth.node.create_appliance(site=site_id, model=model)
 
        if res.status_code == 200:          #if successful
            speech = "The {} appliance was created for the {} site in {}, {}".format(model, site_name, city, country_name)
        elif res.status_code == 400:
            speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
        elif res.status_code == 404:
            speech = "Error: Organization with given id does not exist"
        elif res.status_code == 500:        #If we couldn't create the appliance
            speech = "Error: We could not create the {} appliance for the {} site in {}, {}".format(model, site_name, city, country_name)
        else:
            speech = "Error: Could not connect to SteelConnect"
 
        logging.debug(speech)
    else:
        speech = "The site {} does not exist in {}, {}. No appliances were created.".format(site_name, city,country_name)
    return speech

