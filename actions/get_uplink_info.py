import logging
import requests
from flask import json
from requests.auth import HTTPBasicAuth
from util import get_site_id_by_name

def get_uplink_info (api_auth, parameters, contexts):
    """
    Allow users to get info about a particular uplink
    Need to know the city, site name and country.
    
    :param api_auth: steelconnect api object 
    :type api_auth: SteelConnectAPI 
    :param parameters: json parameters from Dialogflow intent 
    :type parameters: json 
    :return: Returns a response to be read out to user 
    :rtype: string 

    Example Statement: Get uplink information 
    """
    
    uplinks_res = api_auth.uplink.get_uplink_info()
    if uplinks_res.status_code != 200:
        return "Failed to get a list of uplinks"
    
    uplinks = uplinks_res.json()["items"]

    if len(uplinks) == 1:
        uplink_information = uplinks[0]
        information = api_auth.uplink.format_uplink_information(uplink_information)
        speech = "Information for Uplink {}: \n{}".format(uplinks[0]["id"], information)
    elif len(uplinks) > 1:
        uplink_options_response = ''
        uplink_options = []
        count = 1
        for uplink in uplinks:
            uplink_options_response += "Option " + str(count) + ": " + uplink["id"] + '\n' 
            uplink_options.append(uplink["id"])
            count = count + 1
        api_auth.uplink.set_uplink_list(uplink_options)
        speech = "There are multiple uplinks. Please choose a value from the following\n: {}".format(uplink_options_response)
    else:
        return "There were no uplinks found"
    return speech