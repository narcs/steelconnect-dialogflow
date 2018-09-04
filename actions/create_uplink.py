import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def create_uplink(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json object
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        city = parameters["City"]
        uplink_name = parameters["Uplinks"]
        wan_name = parameters["Wans"]

    except KeyError as e:
        error_string = "Error processing createUplink intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    #if uplink_name == "":
    uplink_name = "Uplink"
		
	# Get all the sites and check whether there is a site match given city
    data_sites = api_auth.site.list_sites().json()
    sites = []
    ids = []

    for item in data_sites["items"]:
        if (city.lower() == item["city"].lower()):
            ids.append(item["id"])
            sites.append("{}, {}, {}".format(item["name"], item["city"], item["country"]))
			
	# Error if no sites were found in that city
    if (len(sites) < 1):
        speech = "Error: No site could be found in that city"
        return speech

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be created on
    data_wans = api_auth.wan.list_wans().json()
    wan = " "
    for item in data_wans["items"]:
        if wan_name == item["name"]:
            wan = item["id"]
            break

    # If more than one site is found in that city list them and return to Dialogflow for followup intent to handle
    if (len(sites) > 1):
        speech = "Which site out of these?"
        index = 1
        for site in sites:
            if index == 1:
                speech += "{}".format(site)
            else:
                speech += ", {}".format(site)
            index += 1
        return speech
		
    # Otherwise only one site, so pop it into site
    site_id = ids.pop()
    site = sites.pop()

    # call create uplink api
    res = api_auth.uplink.create_uplink(site_id, uplink_name, wan)

    if res.status_code == 200:
        speech = "An uplink called {} has been created between site: {} and WAN: {} ".format(uplink_name, site,
                                                                                  wan_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not create uplink"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    print(speech)
    print(res.status_code)
    return speech
