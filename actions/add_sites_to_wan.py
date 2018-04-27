import logging

from flask import json
from actions import create_uplink
from ..api.util import find_context_by_name, find_contexts_by_name

def add_sites_to_wan(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :param contexts: json contexts from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        wan_context = find_context_by_name(contexts, "wan_created")["parameters"]
        site_contexts = find_contexts_by_name(contexts, "sitecreated")["parameters"]

        site_success_list = ""
        site_fail_list = ""

        wan_name=wan_context["WANType"]

        for site_context in site_contexts:

            new_parameters = {"SiteTypes": site_context["SiteType"],
                              "City": site_context["City"],
                              "Wans": wan_context["WANType"],
                              "Uplinks": ""}

            res = create_uplink.create_uplink(api_auth, new_parameters)


            if res.startswith("An uplink"):
                site_success_list += new_parameters["City"] + "_" + new_parameters["SiteType"]
                site_success_list += " "
            else:
                site_fail_list += new_parameters["City"] + "_" + new_parameters["SiteType"]
                site_fail_list += " "



    except KeyError as e:
        error_string = "Error processing addSitesToWAN intent. {0}".format(e)

        logging.error(error_string)

        return "Unable to add site to WAN"


    if site_success_list == "":
        speech = "An error occurred, no uplinks were created"
    elif site_fail_list == "":
        speech = "The following sites were added to the {} wan: {}".format(wan_name, site_success_list)
    else:
        speech = "{} where successfully added to the {} wan: Errors occurred adding {} to the wan".format(site_success_list, wan_name, site_fail_list)


    logging.debug(speech)

    return speech

