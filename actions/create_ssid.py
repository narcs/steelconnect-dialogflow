"""
This has not yet been tested or modified since 2017. 
This is potentially deprecated
"""

import logging
from flask import json
from requests.auth import HTTPBasicAuth
import requests


def create_ssid(parameters):
    """
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        id = parameters["id"]
        org = parameters["org"]
        ssid = parameters["ssid"]
        encryption = parameters["encryption"]
        key = parameters["key"]
        authentication = parameters["authentication"]
        eapol_version = parameters["eapol_version"]
        dtim_period = parameters["dtim_period"]

        # API Call Here
        url = 'https://support.riverbed.com/api/scm.config/1.0/org/org-Monash-d388075e40cf1bfd/ssids'
        data = {
            "id": "string",
            "org": "Monash",
            "ssid": ssid,
            "encryption": "wpa2personal",
            "key": key,
            "authentication": "string",
            "eapol_version": "string",
            "dtim_period": "string"
        }
        request = json.dumps(data, indent=4)
        res = requests.post(url, data=request, auth=HTTPBasicAuth('Anthony', 'Anthony'))
        logging.debug(res)
        # Ends Here

        speech = "An SSID has created in site {}".format(ssid.capitalize())

        logging.debug(speech)

        return speech
    except KeyError as e:

        error_string = "Error processing createSSID intent. {0}".format(e)

        logging.error(error_string)

        return error_string


if __name__ == "__main__":
    test = {
        "id": "",
        "org": "",
        "ssid": "test",
        "encryption": "",
        "key": "123",
        "authentication": "",
        "eapol_version": "",
        "dtim_period": ""
    }

    print(create_ssid(test))
