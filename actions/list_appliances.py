import logging 
import requests
from flask import json
from requests.auth import HTTPBasicAuth
 
#  "List all appliances" works but not "list appliances"
def list_appliances(api_auth, parameters, contexts):
    """
    Displays to users all appliances that exists. 
    It will let the know the model, appliance id and on which
    site it is on

    :param api_auth: steelconnect api object 
    :type api_auth: SteelConnectAPI 
    :param parameters: json parameters from Dialogflow intent 
    :type parameters: json 
    :return: Returns a response to be read out to user 
    :rtype: string 
    """
    logging.info("Listing Appliances")
 
    res = api_auth.node.list_appliances()

    if res.status_code == 200:
        data = res.json()["items"]
        num_appliances = len(data)
        appliance_list = []
        for appliance in data:
            appliance_list.append(appliance["model"] + " appliance (ID: " + appliance["id"] + ") on  site ID " + appliance["site"] + "\n")

        if num_appliances == 0:
            speech = "There are no appliances"
        elif num_appliances == 1:
            speech = "There is only one appliance, it is a {} on {} ".format(data[0]["model"], data[0]["site"] )
        elif num_appliances > 1:
            speech = "There are {} appliances. \n{}".format(num_appliances, "".join(appliance_list))
        else:
            speech = "Unknown error occurred when retrieving appliances"
    else:
        speech = "Error: Could not connect to SteelConnect"
    logging.debug(speech)
    
    return speech