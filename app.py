# from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from flask import Flask, request, make_response
import json
import logging

from actions.api import SteelConnectAPI

from actions.create_uplink import create_uplink
from actions.create_site import create_site
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
from actions.create_appliance import create_appliance

app = Flask(__name__)

# Setup up api authentication
try:
    with open("./default-auth.json") as file:
        j = json.load(file)

        app.config["SC_API"] = SteelConnectAPI(j["username"], j["password"], j["realm-url"], j["org-id"])
except IOError:
    j = None
    app.config["SC_API"] = None


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

    if action_type == "CreateSite":
        response = create_site(app.config["SC_API"], parameters)
    elif action_type == "CreateUplink":
        response = create_uplink(app.config["SC_API"],parameters)
    elif action_type == "ListSites":
        response = list_sites(app.config["SC_API"], parameters)
    elif action_type == "ListSites.ListSites-custom":
        response = list_sites_followup(app.config["SC_API"], req["result"]["contexts"][0]["parameters"])
    elif action_type == "ListSites.ListSites-yes":
        parameters["position"] = "all"
        response = list_sites_followup(app.config["SC_API"], None)
    elif action_type == "ListWANs":
        response = list_wans(app.config["SC_API"], parameters, contexts)
    elif action_type == "CreateWAN":
        response = create_wan(app.config["SC_API"], parameters, contexts)
    elif action_type == "RenameWAN":
        response = rename_wan(app.config["SC_API"], parameters, contexts)
    elif action_type == "DeleteWAN":
        response = delete_wan(app.config["SC_API"], parameters, contexts)
    elif action_type == "AddSiteToWAN":
        response = add_site_to_wan(app.config["SC_API"], parameters, contexts)
    elif action_type == "AddSitesToWAN":
        response = add_sites_to_wan(app.config["SC_API"], parameters, contexts)
    elif action_type == "ClearSites":
        response = clear_sites(parameters)
    elif action_type == "CreateZone":
        response = create_zone(app.config["SC_API"], parameters)
    elif action_type == "CreateAppliance":
        response = create_appliance(app.config["SC_API"], parameters)


    # elif action_type == "SomeOtherAction"            # Use elif to add extra functionality
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
