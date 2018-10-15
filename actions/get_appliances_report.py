import logging
from collections import Counter
from flask import json

def get_appliances_report(api_auth, parameters, contexts):
    """
    Allows users to get a quick overview in terms of how many appliances have which status. That is,
    how many are up, down, established and needs attention. 

    Works by getting all the appliances and their associated information. It will iterate through
    each uplink and collect it's status in a Counter. 
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, it takes
                  on no parameters
    
    Returns:
    - speech: A string which has the health check information about the appiiances in the organisation

    Example Prompt:
    - Appliance health check

    """

    appliances_res = api_auth.node.list_appliances()        #Get all applianaces
    if appliances_res.status_code != 200:
        return "Failed to get list of appliances for the health check"

    statuses = Counter()            #Start the counter
    for appliance in appliances_res.json()["items"]:        #Go through each appliance and check it's status
        logging.info("checking appliance {}".format(appliance["id"]))
        appliance_status_check = api_auth.node.get_appliance_info(appliance["id"])

        if appliance_status_check.status_code != 200:   
            logging.warn("Failed to get status check for appliance {}".format(appliance["id"]))
        else:
            statuses[appliance_status_check.json()["state"]] += 1

    status_info = ''
    for key, value in statuses.iteritems():
        status_info = status_info + "Appliances " + key + ": " + str(value) + "\n"

    return "There are currently {} appliances: \n{}".format(str(sum(statuses.values())), status_info)
