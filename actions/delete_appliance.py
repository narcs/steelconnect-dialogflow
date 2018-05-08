import logging
from flask import json
from actions.list_appliances import list_appliances
 
# For now, use id as the way to identify a particular appliance
# This is crap usability, if we have time, find a more usable method in the future
 
def delete_appliance(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object 
    :type api_auth: SteelConnectAPI 
    :param parameters: json parameters from Dialogflow intent 
    :type parameters: json 
    :return: Returns a response to be read out to user 
    :rtype: string 
    """

    appliance_id = parameters["ApplianceID"]
    logging.debug("Attempting to delete Appliance: " + appliance_id)
    
    #Make sure that this appliance exists
    res = api_auth.node.list_appliances()
    data = res.json()["items"]
    
    found = False
    if res.status_code == 200:
        for appliance in data:
            if appliance_id == appliance["id"]:
                appliance_id = appliance["id"]
                found = True
                break
        if found == False:
            return "Error: The Appliance {} does not exist.".format(appliance_id)
    else:
        return "Error: Failed to get a list of appliances"

    # Deleting the appliance
    res = api_auth.node.delete_appliance(appliance_id)
    if res.status_code == 200:
        speech = "Successfully deleted appliance {}".format(appliance_id)
    elif res.status_code == 500:
        speech = "Appliance {} could not be deleted".format(appliance_id)
    else:
        speech = "Error: There was another error while attempting to delete the appliance"
 
    logging.debug(speech)
 
    return speech
 