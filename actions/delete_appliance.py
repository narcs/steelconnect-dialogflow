import logging
from flask import json
from actions.list_appliances import list_appliances
from util import get_site_id_by_name
 
# For now, use id as the way to identify a particular appliance
# This is crap usability, if we have time, find a more usable method in the future
 
 # Delete ewok shadow appliance on banana in Texas, US
 # Delete panda shadow appliance for shop-Helsinki in Helsinki, Finland 

def delete_appliance(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object 
    :type api_auth: SteelConnectAPI 
    :param parameters: json parameters from Dialogflow intent 
    :type parameters: json 
    :return: Returns a response to be read out to user 
    :rtype: string 
    """

    try:
        city = parameters["City"].replace(" ", "")  # .replace() is for locations where there are spaces. E.g. Kuala Lumpur
        site_name = parameters["SiteName"]
        model = parameters["Model"]
        country_code = parameters["Country"]["alpha-2"]
 
    except KeyError as e:
        error_string = "Error processing getting Appliance information intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    site_id = get_site_id_by_name(api_auth, site_name, city,country_code)
    
    #Make sure that this appliance exists
    appliance_list = api_auth.node.list_appliances()
    data = appliance_list.json()["items"]
    if appliance_list.status_code == 200:
        appliances_on_site = []
        for appliance in data:
            if appliance["site"] == site_id and appliance["model"] == model:
                appliances_on_site.append(appliance)
    else:
        return "Error: Failed to get relevant appliances to delete"
    
    if len(appliances_on_site) == 1:
        appliance_id = appliances_on_site[0]["id"]
        res = api_auth.node.delete_appliance(appliance_id)
        if res.status_code == 200:
            speech = "Successfully deleted {} located on {} in {}, {}".format(model, site_name, city, country_code)
        else:
            speech = "Appliance {} could not be deleted".format(appliance_id)
    elif len(appliances_on_site) > 1:
        appliance_options_response = ''
        appliance_options = []
        count = 1
        for appliance in appliances_on_site:
            appliance_options_response += "Option " + str(count) + ": " + appliance["id"] + "\n"
            appliance_options.append(appliance["id"])
            count = count + 1
        api_auth.node.set_appliance_list(appliance_options)
        speech = "There are multiple {} appliances at {}. Please choose a specific appliance to delete from the following: {}".format(model, site_name, appliance_options_response)
    else:
        speech = "Error: There was another error while attempting to delete the appliance"
    logging.debug(speech)
    return speech