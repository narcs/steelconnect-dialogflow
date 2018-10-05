import logging 
from flask import json
 
def list_appliances(api_auth, parameters, contexts):
    """
    Allows users to list all the appliances that are in the organisation, as well as 
    which site they sit on, and it's model type

    Works by calling the list_appliances action defined in api/appliances.py

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. In this case, we
                  obtain nothing

    Returns:
    - speech: A string which has the list of all appliances in the organisation

    Example Prompt:
    - List appliances

    """
    logging.info("Listing Appliances")
 
    res = api_auth.node.list_appliances()
    if res.status_code == 200:
        data = res.json()["items"]
        num_appliances = len(data)

        if num_appliances == 0:
            speech = "There are no appliances"
        elif num_appliances >= 1:
            speech = "There are {} appliances in the organisation: \n".format(num_appliances)
            count = 1
            for appliance in data:
                id = appliance["id"]
                model = appliance["model"]

                if appliance["site"] == None:
                    site_name = "_No Associated Site_" # if the site has been deleted but the appliance still exists, replace deleted site's id with Null. This needs to be done, otherwise, it will cause an error
                else:
                    site = api_auth.site.get_site(appliance["site"])
                    site_name = site.json()["longname"]     #otherwise, display the proper name

                #added leading zeroes in the count variable to help with formatting of data
                speech += "\n{}. ID: {}\n\t  Site: {}\n\t  Model: {}\n".format(str(count).zfill(len(str(num_appliances))), id, site_name, model)            
                count += 1
        else:
            speech = "Unknown error occurred when retrieving appliances"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    return speech