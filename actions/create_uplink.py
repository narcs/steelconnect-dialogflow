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
        site_type = parameters["SiteTypes"]
        city = parameters["City"]
        uplink_name = parameters["Uplinks"]
        wan_name = parameters["Wans"]

    except KeyError as e:
        error_string = "Error processing createUplink intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all the sites and check whether there is a site match given city and site type
    if uplink_name == "":
        uplink_name = "Uplink";
    data_sites = api_auth.site.list_sites().json()
    print(data_sites)
    site = " "
    for item in data_sites["items"]:
        if city + site_type in item["id"]:
            site = item["id"]
            break

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be created on
    data_wans = api_auth.wan.list_wans().json()
    wan = " "
    for item in data_wans["items"]:
        if wan_name == item["name"]:
            wan = item["id"]
            break

    # call create uplink api
    res = api_auth.uplink.create_uplink(site, uplink_name, wan)

    if res.status_code == 200:
        speech = "An uplink called {} has been created between site {}_{} and {} wan".format(uplink_name, city, site_type,
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
