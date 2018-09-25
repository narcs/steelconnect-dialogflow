import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def create_uplink_select_site(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json object
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        site_type = parameters["SiteNames"]
        wan_name = contexts[0]["parameters"]["Wans"]
    except KeyError as e:
        error_string = "Error processing createUplink intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    uplink_name = "Uplink"

    # Get all the sites and check whether there is a site match given city
    data_sites = api_auth.site.list_sites().json()
    id = ""
    found = False

    for item in data_sites["items"]:
        if (site_type == item["name"]):
            id = item["id"]
            found = True
            break
        
    #Check if site was found and error if not
    if not found:
        speech = "Error: Site {} was not found".format(site_type)
        return speech

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be created on
    data_wans = api_auth.wan.list_wans().json()
    wan = " "
    for item in data_wans["items"]:
        if wan_name == item["name"]:
            wan = item["id"]
            break

    # Make the API call to SteelConnect
    res = api_auth.uplink.create_uplink(id, uplink_name, wan)

    if res.status_code == 200:
        speech = "An uplink called {} has been created between site: {} and WAN: {} ".format(uplink_name, site_type,
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