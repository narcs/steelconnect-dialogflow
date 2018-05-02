import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def clear_sites(api_auth, parameters, contexts):
    """
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user (Successful or Failure)
    :rtype: string
    """
    try:

        # First Get the list of sites
        url = 'https://monash.riverbed.cc/api/scm.config/1.0/org/org-Monash-d388075e40cf1bfd/sites'
        res = requests.get(url, auth=HTTPBasicAuth('Shaylin', 'sche259'))
        data = res.json()

        # Loop and delete
        for site in data['items']:
            res = requests.delete('https://monash.riverbed.cc/api/scm.config/1.0/site/'+site['id'], auth=HTTPBasicAuth('Shaylin', 'sche259'))
            logging.debug(res)

        if res.status_code == 200:
            speech = "All Sites Cleared"
        elif res.status_code == 500:
            speech = "Error: Could not find sites"
        else:
            speech = "Error: Could not connect to SteelConnect"

        logging.debug(speech)

        return speech

    except KeyError as e:

        error_string = "Error processing clearSites intent. {0}".format(e)

        logging.error(error_string)

        return error_string

