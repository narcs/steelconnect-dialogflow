import logging
from flask import json
from actions.list_appliances import list_appliances
from util import get_site_id_by_name, APIError

def delete_appliance(api_auth, parameters, contexts):
    """
    Allows users to delete an appliance on a site. 
    In order for them to do so, we need to know the city, site name model and country code. 

    Works by checking if the site exists. If it exists, it gets the parameters, and with the 
    parameters, it calls the SteelConnectAPI, and deletes the appliance. If there are multiple 
    appliances of the same model and on the same site, user will be prompted to enter a number
    to delete the appropriate site (This is in the delete_appliance_followup.py file. 

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: In which city the site is located in
        > country_code: The country code of the country where the site is located 
        > model: The model of the appliance the user wants to delete
        > site_name: the name of the site the user wants to remove the appliance from
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - Delete panda shadow appliance for shop-Helsinki in Helsinki, Finland

    """

    try:
        city = parameters["City"]
        site_name = parameters["SiteName"]
        model = parameters["Model"]
        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]

    except KeyError as e:
        error_string = "Error processing getting Appliance information intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    try:
        site_id = get_site_id_by_name(api_auth, site_name, city,country_code)       # Get the site id based of the site name, city and country
    except APIError as E:
        return str(E)

    #Make sure that this appliance exists
    appliance_list = api_auth.node.list_appliances()
    data = appliance_list.json()["items"]
    if appliance_list.status_code == 200:
        appliances_on_site = []         
        for appliance in data:
            if appliance["site"] == site_id and appliance["model"] == model: #Gets a list of appliances that match the model and site
                appliances_on_site.append(appliance)
    else:
        return "Error: Failed to get relevant appliances to delete"
    
    if len(appliances_on_site) == 1:            #If we have only one appliance that matches the site and model, then delete the appliance
        appliance_id = appliances_on_site[0]["id"]
        res = api_auth.node.delete_appliance(appliance_id)
        if res.status_code == 200:                  #If we are able to delete the appliance
            speech = "The {} appliance on the {} site in {}, {} was deleted".format(model, site_name, city, country_name)
        else:                   #If we are unable to for whatever reason
            speech = "The {} appliance on the {} site located in {}, {} could not be deleted".format(model, site_name, city, country_name )
    elif len(appliances_on_site) > 1:           #If there are more than one appliances that matches the site and model, then prepare the response options, and call delete_appliance_followup.py
        appliance_options_response = ''
        appliance_options = []
        count = 1
        for appliance in appliances_on_site:
            appliance_options_response += "Option " + str(count) + ": " + appliance["id"] + "\n"
            appliance_options.append(appliance["id"])
            count = count + 1
        api_auth.node.set_appliance_list(appliance_options)         #Saves the options to be deleted
        speech = "There are multiple {} appliances at {}. Please choose a specific appliance to delete from the following: {}".format(model, site_name, appliance_options_response)
    else:
        speech = "Error: There was another error while attempting to delete the appliance"
    logging.debug(speech)
    return speech