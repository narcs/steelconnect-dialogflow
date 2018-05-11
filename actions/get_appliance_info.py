import logging
import requests
from flask import json
from requests.auth import HTTPBasicAuth
from util import get_site_id_by_name

def get_appliance_info(api_auth, parameters, contexts):
    try:
        city = parameters["City"].replace(" ", "")  # .replace() is for locations where there are spaces. E.g. Kuala Lumpur
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
            speech = "Information for {} appliance on {} located in {}, {}:\n{}".format(model, site_name, city, country_code, information)
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
