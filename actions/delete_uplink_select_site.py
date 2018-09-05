import logging

from flask import json
from requests.auth import HTTPBasicAuth
import requests


def delete_uplink_select_site(api_auth, parameters, contexts):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json object
    :return: Returns a response to be read out to user
    :rtype: string
    """
    try:
        site_type = parameters["SiteNames"]
        wan_name = contexts[0]["parameters"]["Wans"]
    except KeyError as e:
        error_string = "Error processing deleteUplink-followup intent. {0}".format(e)
        logging.error(error_string)
        return error_string


    # Get all the sites and check whether there is a site match given city
    data_sites = api_auth.site.list_sites().json()
    site_id = ""
    found = False

    for item in data_sites["items"]:
        if (site_type == item["name"]):
            site_id = item["id"]
            found = True
            break

    #Check if site was found and error if not
    if not found:
        speech = "Error: Site {} was not found".format(site_type)
        return speech

    # Get all the wans and check whether there is a wan match target wan user want the uplink to be deleted
    data_wans = api_auth.wan.list_wans().json()
    wan = " "
    for item in data_wans["items"]:
        if wan_name == item["name"]:
            wan = item["id"]
            break

    # Get uplink info of that site
    data_uplinks = api_auth.uplink.get_uplink_info(site_id).json()
    uplinks = []
    for item in data_uplinks["items"]:
        if (wan == item["wan"]):
            uplinks.append(item)

    # If uplinks[] is empty then return error that no uplink was found
    if (len(uplinks) < 1):
        return "Error: No Uplink from that site to that WAN was found"

    # Otherwise delete the last one
    # This is because all the uplinks between the same site and WAN are essentially the same
    uplink = uplinks.pop()
    uplink_id = uplink["id"]
    uplink_name = uplink["name"]

    # call delete uplink api
    res = api_auth.uplink.delete_uplink(uplink_id)


    if res.status_code == 200:
        speech = "An uplink called {} between site: {} and WAN: {} has been deleted".format(uplink_name, site_type,
                                                                                  wan_name)
    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)
    print(speech)
    print(res.status_code)
    return speech