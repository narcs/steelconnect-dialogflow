# from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from flask import Flask, request, make_response
import json
import logging

from api import SteelConnectAPI

from actions.create_site import create_site
from actions.create_uplink import create_uplink
from actions.list_sites import list_sites
from actions.list_sites_followup import list_sites_followup
from actions.list_wans import list_wans
from actions.create_wan import create_wan
from actions.rename_wan import rename_wan
from actions.delete_wan import delete_wan
from actions.add_site_to_wan import add_site_to_wan
from actions.add_sites_to_wan import add_sites_to_wan
from actions.clear_sites import clear_sites
from actions.create_zone import create_zone
from actions.list_appliances import list_appliances
from actions.list_appliances_followup import list_appliances_followup
from actions.delete_appliance import delete_appliance
from actions.delete_appliance_followup import delete_appliance_followup
from actions.uplink import list_uplinks
from actions.get_appliance_info import get_appliance_info
from actions.get_appliance_info_followup import get_appliance_info_followup

from actions.create_appliance import create_appliance

app = Flask(__name__)
app.Debug = True


# Setup up api authentication
try:
    with open("./default-auth.json") as file:
        j = json.load(file)

        app.config["SC_API"] = SteelConnectAPI(j["username"], j["password"], j["realm-url"], j["org-id"])
except IOError:
    j = None
    app.config["SC_API"] = None


# Register actions.
# 
# Actions are functions with the signature `(api_auth, parameters, contexts) -> response_string`
actions = {}

def register_action(name, func):
    actions[name] = func

def list_sites_followup_custom(api_auth, parameters, contexts):
    return list_sites_followup(api_auth, contexts[0]["parameters"], contexts)

def list_sites_followup_yes(api_auth, parameters, contexts):
    return list_sites_followup(api_auth, None, contexts)

def list_appliances_followup_yes(api_auth, parameters, contexts):
    return list_appliances_followup(api_auth, None, contexts)

def list_appliances_followup_custom(api_auth, parameters, contexts):
    return list_appliances_followup(api_auth, contexts[0]["parameters"], contexts)

def get_appliance_info_followup_custom(api_auth, parameters, contexts):
    return get_appliance_info_followup(api_auth, contexts[0]["parameters"], contexts)

def delete_appliance_followup_custom(api_auth, parameters, contexts):
    return delete_appliance_followup(api_auth, contexts[0]["parameters"], contexts)

register_action("CreateSite", create_site)
register_action("CreateUplink", create_uplink)
register_action("ListSites", list_sites)
register_action("ListSites.ListSites-custom", list_sites_followup_custom)
register_action("ListSites.ListSites-yes", list_sites_followup_yes)
register_action("ListWANs", list_wans)
register_action("CreateWAN", create_wan)
register_action("RenameWAN", rename_wan)
register_action("DeleteWAN", delete_wan)
register_action("AddSiteToWAN", add_site_to_wan)
register_action("AddSitesToWAN", add_sites_to_wan)
register_action("ClearSites", clear_sites)
register_action("CreateZone", create_zone)
register_action("ListUplinks", list_uplinks)
register_action("ListAppliances", list_appliances)
register_action("ListAppliances.ListAppliances-custom", list_appliances_followup_custom)
register_action("ListAppliances.ListAppliances-yes",list_appliances_followup_yes)
register_action("DeleteAppliance", delete_appliance)
register_action("DeleteAppliance.DeleteAppliance-custom", delete_appliance_followup_custom)
register_action("GetApplianceInfo", get_appliance_info)
register_action("GetApplianceInfo.GetApplianceInfo-custom", get_appliance_info_followup_custom)
register_action("CreateAppliance", create_appliance)

@app.route('/')
def home():
    return "This app works"


@app.route('/webhook/', methods=['POST'])
def webhook():
    """
    Extracts the intent, action and paramaters and passes them to the handling method.
    :return: Returns a json formatted response containing the text to be read back to the user
    :rtype: json
    """
    req = request.get_json(silent=True, force=True)

    logging.debug("Request\n" + json.dumps(req, indent=4))

    try:
        action_type = req["result"]["action"]
        intent_type = req["result"]["metadata"]["intentName"]
        parameters = req["result"]["parameters"]
        contexts = req["result"]["contexts"]
    except KeyError as e:
        logging.error("Error processing request {}".format(e))
        return format_response("There was an error processing your request")

    # Call the given action, if it exists.
    logging.debug("Got action: {}".format(action_type))
    if action_type in actions:
        response = actions[action_type](app.config["SC_API"], parameters, contexts)
    else:
        response = "Error: This feature has not been implemented yet"
        logging.error("Not implemented error action: {} intent: {}".format(action_type, intent_type))

    return format_response(response)                        # Correctly format the text response into json for Dialogflow to read out to the user


def format_response(speech):
    """
    :param speech: A text string to be read out to the user
    :type speech: string
    :return: Returns a json formatted response
    :rtype: json
    """
    response = {
        "speech": speech,
        "displayText": speech,
        "source": "steelconnect"
    }

    response = json.dumps(response, indent=4)
    logging.debug(response)
    r = make_response(response)
    r.headers['Content-Type'] = 'application/json'

    return r


if __name__ == '__main__':
    # Only used when running locally, uses entrypoint in app.yaml when run on google cloud
    app.run(debug=True, port=8080, host='127.0.0.1')
