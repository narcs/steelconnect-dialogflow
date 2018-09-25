import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def delete_uplink(api_auth, parameters, contexts):
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
        wan_name = parameters["Wans"]

    except KeyError as e:
        error_string = "Error processing deleteUplink intent. {0}".format(e)
        logging.error(error_string)
        return error_string
		
	# Get all the sites and check whether there is a site match given city
    data_sites = api_auth.site.list_sites().json()
    sites = []
    ids = []

    for item in data_sites["items"]:
        if (city.lower() == item["city"].lower()):
            ids.append(item["id"])
            sites.append("{}".format(item["name"]))
			
	# Error if no sites were found in that city
    if (len(sites) < 1):
        speech = "Error: No site could be found in that city"
        return speech

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be deleted
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

    # Get uplink info of that site
    data_uplinks = api_auth.uplink.get_uplink_info(site_id).json()
    uplinks = []
    for item in data_uplinks["items"]:
        if (wan == item["wan"]):
            uplinks.append(item)

    # If uplinks[] is empty then return error that no uplink was found
    if (len(uplinks) < 1):
        return "Error: No Uplink from that site to that WAN was found"

    # Otherwise delete the last one
    # This is because all the uplinks between the same site and WAN are essentially the same
    uplink = uplinks.pop()
    uplink_id = uplink["id"]
    uplink_name = uplink["name"]

    # call delete uplink api
    res = api_auth.uplink.delete_uplink(uplink_id)

    if res.status_code == 200:
        speech = "Uplink called {} between site: {} and WAN: {} has been deleted".format(uplink_name, site,
                                                                                  wan_name)
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    print(speech)
    print(res.status_code)
    return speech