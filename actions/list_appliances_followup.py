import logging
from flask import json

def list_appliances_followup(api_auth, parameters, contexts):
    """ 
    :param api_auth: steelconnect api object 
    :type api_auth: SteelConnectAPI 
    :param parameters: json parameters from Dialogflow intent 
    :type parameters: json 
    :return: Returns a response to be read out to user 
    :rtype: string 
    """

    # Get all appliances and return a response based on the number of appliances
    res = api_auth.node.list_appliances()
 
    if res.status_code == 200:
        data = res.json()["items"]
        num_appliances = len(data)

        if parameters:
            try:
                number = int(parameters["number"])
                position = parameters["position"]
            except KeyError as e:
                logging.error("Error processing list_appliances_followup intent. {0}".format(e))
 
                return "There was an error fulfilling your request"

        else:
            number = num_appliances
            position = "all"
 
        speech = ""

        if number > num_appliances:
            number = num_appliances
 
        if position == "first":
            data = data[:number]
        elif position == "last":
            data = data[-number]
        elif position == "all":
            pass
        else:
            logging.error("Error processing list_appliance_followup intent. Unrecognised position: {}".format(position))
 
            return "There was an error fulfilling your request"

        for appliance in data:
            site = appliance["site"]
            id = appliance["id"]
            model = appliance["model"]
 
            speech += ", Node ID: {}\nSite: {}\nAppliance Model:{}".format(id, site, model)
 
        speech = speech[2:] + "."

    else:
        speech = "Error: Could not connect to SteelConnect"
    
    logging.debug(speech)
 
    return speech