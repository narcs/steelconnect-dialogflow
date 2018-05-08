import logging
import requests
from flask import json
from requests.auth import HTTPBasicAuth
from util import get_site_id_by_name

# Get information about appliances on banana in Tokyo, Japan

def get_appliance_info(api_auth, parameters, contexts):
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
        appliance_id = appliance["id"]
        res = api_auth.node.get_appliance_info(node_id= appliance_id)
        if res.status_code == 200:
            appliance_info = res.json()
            information = []
            information.append("Appliance ID: " + str(appliance_id) + "\n")
            information.append("Model: " + model + "\n")
            information.append("Organisation: " + str(appliance_info["org"] + "\n"))
            information.append("Serial: " + str(appliance_info["serial"]) + "\n")
            information.append("Site: " + str(site_name) + "\n")
            information.append("Location: " + city + ', ' + country_code)
            information.append("Uptime: " + str(appliance_info["uptime"]) + "\n")
            information.append("CPU Load: " + str(appliance_info["cpu_load"]) + "\n")
            information.append("Mem Load" + str(appliance_info["mem_load"]) + "\n")
            information.append("State: " + str(appliance_info["state"]) + "\n")
            information.append("Last Online: " + appliance_info["last_online"] + "\n")
            # information = "Appliance ID: " + str(appliance_id) + "\nModel: " + model + "\n" + org + 
            # information = "Appliance ID: {}\nModel: {}\nOrganisation: {}\nSerial: {}\nSite: {}\nLocation: {},{}".format(appliance_id, model, org, serial, site_name)
            speech = "Information for {} appliance on {} located in {}, {}:\n{}".format(model, site_name, city, country_code, information)
        else:
            return "Error: Failed to get information about appliances"          #this error is for the specific appliance
    # elif len(appliances_on_site) > 1:       #If we have more than one appliance that matches the spec

    else:   #Just in case, though not likely
        return "Error: Invalid number of appliances"
    return speech
    # if site_id:
    #     res = api_auth.node.get_appliance(node_id)
"""


def create_appliance_new(api_auth, parameters, contexts):
    if site != "":
        # return (str(if(site_id)))
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


"""