import logging
from collections import Counter
from flask import json

def get_uplinks_report (api_auth, parameters, contexts):
    """
    Allows users to get a quick overview in terms of how many uplinks have which status. That is,
    how many are up, down, established and needs attention. 

    Works by getting all the uplinks and their associated information. It will iterate through
    each uplink and collect it's status in a Counter. 
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, it takes
                  on no parameters
    
    Returns:
    - speech: A string which has the health check information about the uplinks in the organisation

    Example Prompt:
    - Uplinks health check

    """

    uplinks_res = api_auth.uplink.get_uplink_info()
    if uplinks_res.status_code != 200:
        return "Failed to get list of uplinks for the health check"
    
    statuses = Counter()
    for uplink in uplinks_res.json()["items"]:
        logging.info("checking uplink {}".format(uplink["id"]))
        statuses[uplink["state"]] += 1
    
    status_info = ''
    for key, value in statuses.iteritems():
        if key == 0:
            status_info = status_info + "Uplinks up: " + str(value) + "\n "
        else:
            status_info = status_info + "Uplinks that need attention: " + str(value) + "\n "
            
    return "There are currently {} uplinks: \n{}".format(str(sum(statuses.values())), status_info)
