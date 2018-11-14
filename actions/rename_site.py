import logging
from flask import json
from actions.util import *

def rename_site(api_auth, parameters, contexts):
    """
    Allows users to rename an existing site

    Works by getting the site id from the sitename, country nand city. From there it changes the
    old site name to the new site name using the rename_site method defined in api/sites
    
    Parameters:
    - api_auth: SteelConnect API object, it contains authentication log in details
    - parameters: The json parameters obtained from the Dialogflow Intent. It obtains the following:
        > city: The city where the user wants to create the site
        > country_code: The country code of where the user wants to create the site
            + The country name will be obtained from the country code, and will not be directly
              retrieved from the user
        > old_name: the name of the site the user wants to change
        > new_name: the new name of the site the user wants to give
    
    Returns:
    - speech: A string which lets the user know if the site has been renamed or not

    Example Prompt:
    - Rename Shop in Perth, Australia to Branch

    """
    
    try:
        old_name = parameters["OldName"]
        new_name = parameters["NewName"]
        city = parameters["City"]

        country_code = parameters["Country"]["alpha-2"]
        country_name = parameters["Country"]["name"]
        
    except KeyError as e:

        error_string = "Error processing renameSite intent. {0}".format(e)

        logging.error(error_string)

        return error_string

    # Grab site id by name, city and country
    try:
        site_id = get_site_id_by_name(api_auth, old_name, city, country_code)
    except APIError as e:
        return str(e)

    # Renaming site
    res = api_auth.site.rename_site(site_id, new_name, new_name, city, country_code)

    if res.status_code == 200:
        speech = "Site {} in {} {} has been successfully renamed to {}".format(old_name, city, country_name, new_name)
    elif res.status_code == 400:
        speech = "Invalid parameters: {}".format(res.json()["error"]["message"])
    elif res.status_code == 500:
        speech = "Error: Could not rename site"
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech