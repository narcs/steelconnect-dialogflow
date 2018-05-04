import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests
# import app


def create_appliance(api_auth, parameters, contexts):
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
        model = parameters["Model"]

    except KeyError as e:
        error_string = "Error processing create Appliance intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Get all sites and check whether site exists
    data_sites = api_auth.site.list_sites().json()
    site = ""
    for item in data_sites["items"]:
        if city + site_type in item["id"]:
            site = item["id"]
            break

    # nodes = api_auth.list_nodes().json()
    # print(nodes)
    if site != "":

        # Call create_appliance in SteelConnectAPI
        res = api_auth.node.create_appliance(site=site, model=model)

        if res.status_code == 200:
            speech = "Appliance: {} created for site: {}, {}".format(model, city, site_type)
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
        speech = "Invalid site {}, {}".format(city, site_type)
    return speech

# auth = app.SteelConnectAPI("Anthony", "Anthony", "monash.riverbed.cc", "org-Monash-d388075e40cf1bfd")
# param = {
#     "City": "Bendigo",
#     "SiteTypes": "shop",
#     "Model": "panda"
# }
# create_appliance(api_auth=auth, parameters=param)

# List of models: raccoon, koala, ursus, panda, ewok, grizzly, panther, cx570, cx770, cx3070, aardvark, sloth, kodiak
