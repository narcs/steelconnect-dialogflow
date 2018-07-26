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

    Example Statement: Get uplink information on Mothership in Alice Springs, Australia
    """
# Get info about uplink at site blah
    try:
        site_name = parameters["SiteName"]
        # Need city and country as well because you want to hone in on which site
        city = parameters["City"]
        country_code = parameters["Country"]["alpha-2"]
    except KeyError as e:
        error_string = "Error processing getting Appliance information intent. {0}".format(e)
        logging.error(error_string)
        return error_string    

    # Get all sites and check whether the site name exists in that location
    site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    
    # See if there are uplinks on the site
    uplink_list = api_auth.uplink.list_uplinks()
    if uplink_list.status_code == 200:
        data = uplink_list.json()["items"]
        uplinks_on_site = []
        for uplink in data:
            if uplink["site"] == site_id:
                uplinks_on_site.append(uplink)
    else:
        return "Error: Failed to get uplinks on specified site"
    
    # If there are uplinks on the site then collect the information and spit it out
    if len(uplinks_on_site) > 0:
        res = api_auth.uplink.get_uplink_info(site_id)
        if res.status_code == 200:
            information = []
            count = 1
            uplink_info = res.json()
            for uplink_data in uplink_info["items"]:
                information.append('Uplink Number ' + str(count) + ': \n')
                information.append(api_auth.uplink.format_uplink_information(uplink_data))
                information.append('\n')
                count = count + 1
            speech = "There are {} uplinks on {}, located in {}, {}: \n {}".format(len(uplinks_on_site), site_id, city, country_code, ''.join(information))
        else:
            return "Error: Failed to get information about uplinks"        
    else:
        return "There were no uplinks found on {}, located in {}, {}. Please try a different site name or location.".format(site_name, city, country_code)
    return speech