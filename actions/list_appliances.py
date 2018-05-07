import logging 
import requests
from flask import json
from requests.auth import HTTPBasicAuth
 
#  "List all appliances" works but not "list appliances"
def list_appliances(api_auth, parameters, contexts):
 
    logging.info("Listing Appliances")
    org = parameters["organisation"]
 
    res = api_auth.node.list_appliances()

    if res.status_code == 200:
        data = res.json()["items"]
        num_appliances = len(data)
 
        if num_appliances == 0:
            speech = "There are no appliances in the {} organisation".format(org)
        elif num_appliances == 1:
            speech = "There is one appliance in the {} organisation, it is a {} on {} ".format(org, data[0]["model"], data[0]["site"] )
        elif num_appliances > 1:
            speech = "There are {} appliances in the {} organisation, would you like to list all of them?".format(num_appliances, org)
        else:
            speech = "Unknown error occurred when retrieving appliances"
    else:
        speech = "Error: Could not connect to SteelConnect"
    logging.debug(speech)
    
    return speech