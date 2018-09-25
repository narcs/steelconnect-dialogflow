import logging
from collections import Counter
from flask import json

def get_uplinks_report (api_auth, parameters, contexts):

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
