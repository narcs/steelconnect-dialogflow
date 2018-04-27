import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def create_zone(api_auth, parameters):
    """
    :param api_auth: SteelConnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        city = parameters["City"]
        site_type = parameters["SiteTypes"]

    except KeyError as e:
        error_string = "Error processing create Zone intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all sites and check whether site exists
    data_sites = api_auth.api_site.list_sites().json()
    site = ""
    for item in data_sites["items"]:
        if city + site_type in item["id"]:
            site = item["id"]
            break
    if site != "":

        # Get all Zones and generate a new zone number
        data_zones = api_auth.api_zone.list_zones().json()
        zone = 1
        for item in data_zones["items"]:
            if "Zone_" in item["name"]:
                chk = item["name"]
                if chk[5:].isdigit():
                    if int(chk[5:]) >= zone:
                        zone = int(chk[5:]) + 1
        name = "Zone_" + str(zone)

        # Call create_zone in SteelConnectAPI
        res = api_auth.api_zone.create_zone(name=name, site=site)

        if res.status_code == 200:
            speech = "Zone: {} created for site: {}, {}".format(name, city, site_type)
        elif res.status_code == 400:
            speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
        elif res.status_code == 500:
            speech = "Error: Could not create Zone"
        else:
            speech = "Error: Could not connect to SteelConnect"

        logging.debug(speech)
    else:
        speech = "Invalid site {}, {}".format(city, site_type)
    return speech

# auth = app.SteelConnectAPI("Finn", "Kalapuikot", "monash.riverbed.cc", "org-Monash-d388075e40cf1bfd")
# param = {
#     "City": "Bendigo",
#     "SiteTypes": "site"
# }
# create_zone(api_auth=auth, parameters=param)