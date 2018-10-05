import logging
import requests
from flask import json
from requests.auth import HTTPBasicAuth
from util import get_site_id_by_name

def get_appliance_info(api_auth, parameters, contexts):
    """
    Allows users to get detailed information about a particular appliance

    Works by checking if the site exists. If it exists, it gets the parameters, and with the 
    parameters, it calls the SteelConnectAPI, and retrieves the information about the appliance. If
    there are multiple appliances of the same model and on the same site, the user will be prompted 
    to enter a number to delete the appropriate site (This is in the get_appliance_info_followup.py 
    file. 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > model: The model of the appliance the user wants to find information about
        > site_name: the name of the site the user wants to get appliance information about

    Returns:
    - speech: A string which has the list of all sites in the organisation

    Example Prompt:
    - Get information on ewok shadow appliance for chicken in Tokyo, Japan

    """
    try:
        city = parameters["City"]
        site_name = parameters["SiteName"]
        model = parameters["Model"]
        country_code = parameters["Country"]["alpha-2"]
 
    except KeyError as e:
        error_string = "Error processing getting Appliance information intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all sites and check whether site exists
    site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    
    appliance_list = api_auth.node.list_appliances()        #Get all appliances first
    if appliance_list.status_code == 200:
        data = appliance_list.json()["items"]
        appliances_on_site = []
        for appliance in data:                          #Get appliances that matches the info given
            if appliance["site"] == site_id and appliance["model"] == model:
                appliances_on_site.append(appliance)
    else:
        return "Error: Failed to get relevant appliances"

    if len(appliances_on_site) == 1:        #If only one appliance matches the spec
        appliance_id = appliances_on_site[0]["id"]
        res = api_auth.node.get_appliance_info(node_id= appliance_id)
        if res.status_code == 200:
            appliance_info = res.json()
            information = api_auth.node.format_appliance_information(appliance_info)
            speech = "Information for {} appliance on {} located in {}, {}:\n{}".format(model, site_name, city, country_code, ''.join(information))
        else:
            return "Error: Failed to get information about appliances"          #this error is for the specific appliance
    elif len(appliances_on_site) > 1:       #If we have more than one appliance that matches the spec
        appliance_options_response = ''
        appliance_options = []
        count = 1
        for appliance in appliances_on_site:
            appliance_options_response += "Option " + str(count) + ": " + appliance["id"] + '\n'
            appliance_options.append(appliance["id"])
            count = count + 1
        api_auth.node.set_appliance_list(appliance_options)         #Store the list of appliances on the chosen site
        speech = "There are multiple {} appliances at {}. Please choose a value from one of the following: {}".format(model, site_name, appliance_options_response)
    else: #If we couldn't find any appliances
        return "There were no {} appliances found on {} located in {}, {}. Please try a different appliance, site name, or location".format(model, site_name, city, country_code)
    return speech
