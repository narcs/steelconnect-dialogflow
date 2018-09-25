import logging
from collections import Counter

from flask import json

def get_appliances_report(api_auth, parameters, contexts):
    """
    This action helps to retrieve status information used in the SteelConnect
    health check.
    
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    appliances_res = api_auth.node.list_appliances()
    if appliances_res.status_code != 200:
        return "Failed to get list of appliances for the health check"

    statuses = Counter()
    for appliance in appliances_res.json()["items"]:
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
