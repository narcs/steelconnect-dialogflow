import logging
from flask import json
from actions.util import get_site_id_by_name, APIError

def delete_site(api_auth, parameters, contexts):
    """
    Allows users to delete a site 
    In order for them to do so, we need to know the city, site name and country code. 

    Works by getting the parameters, and calling the SteelConnect API with the parameters to delete
    the site. It checks to see if the site does exist, and if it does, it will delete the site. It
    not, it will let the user know that the site doesn't exist

    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: The city where the user wants to delete the site
        > country_code: The country code of where the user wants to delete the site
            + The country name will be obtained from the country code, and will not be directly
              retrieved from the user
        > site_name: A name that the user gives the site they want to delete 
    
    Returns:
    - speech: A string which has the response to be read/printed to the user

    Example Prompt:
    - delete a site called bulbasaur in Hobart, Australia

    """
    
    try:
        site_name = parameters["name"]
        city = parameters["City"]
        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:
        error_string = "Error processing deleteSite intent. {0}".format(e)
        logging.error(error_string)
        return error_string

    # Grab site id by name, city and country
    try:
        site_id = get_site_id_by_name(api_auth, site_name, city, country_code)
    except APIError as e:
        return str(e)

    # Deleting site
    res = api_auth.site.delete_site(site_id)

    if res.status_code == 200:
        speech = "The site {} located in {}, {} has been successfully deleted".format(site_name, city, country_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: We could not delete the {} site located in {}, {}".format(site_name, city, country_name)
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech