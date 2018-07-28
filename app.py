# from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from flask import Flask, request, make_response, render_template, url_for, redirect
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from api import SteelConnectAPI
from config import firestore_project_id

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
from actions.delete_appliance import delete_appliance
from actions.delete_appliance_followup import delete_appliance_followup
from actions.uplink import list_uplinks
from actions.get_appliance_info import get_appliance_info
from actions.get_appliance_info_followup import get_appliance_info_followup

from actions.create_appliance import create_appliance

app = Flask(__name__)
app.Debug = True

firestore_API = "https://firestore.googleapis.com/v1beta1/projects/{}/databases/(default)/documents".format(firestore_project_id)
collection = "Accounts"

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
    # Checked authentication
    if not app.config["SC_API"]:
        response = "Not authenticated."
        return format_response(response)

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

def validate_username_password(firestore_collection_api, username, password):
    res = requests.get(firestore_collection_api + username)
    if res.status_code == 200:
        data = res.json()["fields"]
        hashed_password = data["password"]["stringValue"]
        if check_password_hash(hashed_password, password):
            return data
        else:
            return "Wrong password"
    else:
        return "Username not found"

def check_passwords_match(password_1, password_2):
    if password_1 == password_2:
        return True
    else:
        return "Password confirmation does not match"

@app.route("/authenticate", methods=["GET", "POST"])
def authenticate(authenticated=None):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Get data from Firestore
        data = validate_username_password(firestore_API + "/{}/".format(collection), username, password)
        if isinstance(data, str):
            return data
        else:
            # Get realm
            realms = data["realms"]["mapValue"]["fields"]
            realm = realms.keys()[0] # Get first key TODO: allow users to choose realm
            realm = realm.encode("ascii")
            # Get organisation id
            org_ids = realms[realm]["arrayValue"]["values"]
            org_id = org_ids[0]["stringValue"] # Get first org_id TODO: allow users to choose org_id
            org_id = org_id.encode("ascii")
            print(realm, org_id)
            app.config["SC_API"] = SteelConnectAPI(username, password, realm, org_id)
            return "success!"
    if app.config["SC_API"]:
        authenticated = app.config["SC_API"]
    return render_template("authenticate.html", authenticated=authenticated)

@app.route("/status")
def status():
    if not app.config["SC_API"]:
        return "Currently not logged in."
    else:
        return "Logged in as: {}".format(app.config["SC_API"].auth.username)

@app.route("/logout")
def logout():
    app.config["SC_API"] = None
    return redirect(url_for("authenticate"))

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        realm = request.form["realm"]
        org_id = request.form["org_id"]
        passwords_match = check_passwords_match(password, password_confirm)
        if isinstance(passwords_match, str):
            return passwords_match
        else:
            document_id = username
            realms = {
                realm: [
                    org_id,
                ],
            }
            realm_request_body = create_firestore_realms_request_body(realms)
            hashed_password = generate_password_hash(password)
            password_request_body = create_firestore_password_request_body(hashed_password)
            request_body = create_firestore_request_body(realm_request_body, password_request_body)
            request_url = "{}{}{}{}".format(firestore_API, "/{}".format(collection), "?documentId=", document_id)
            res = requests.post(request_url, json=request_body)
            if res.status_code == 200:
                return "Done"
            elif res.status_code == 409:
                return "User already exists"
            else:
                return "Error"

    return render_template("create.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_password = request.form["new_password"]
        new_password_confirm = request.form["new_password_confirm"]
        # Validate username and password
        data = validate_username_password(firestore_API + "/{}/".format(collection), username, password)
        if isinstance(data, str):
            return data
        else:
            passwords_match = check_passwords_match(new_password, new_password_confirm)
            if isinstance(passwords_match, str):
                return passwords_match
            else:
                # Update password
                res = requests.get(firestore_API + "/{}/".format(collection) + username)
                if res.status_code == 200:
                    data = res.json()
                    hashed_password = generate_password_hash(new_password)
                    data["fields"]["password"]["stringValue"] = hashed_password 
                    del data["name"]
                    del data["createTime"]
                    del data["updateTime"]
                    res = requests.patch(firestore_API + "/{}/".format(collection) + username + "?currentDocument.exists=true", json=data)
                    if res.status_code == 200:
                        return "Password successfully changed"
    return render_template("change_password.html")

def create_firestore_realms_request_body(new_realms):
    body = {
        "realms": {
            "mapValue": {
                "fields": {}
            }
        }
    }
    for realm in new_realms:
        body["realms"]["mapValue"]["fields"][realm] = {}
        body["realms"]["mapValue"]["fields"][realm]["arrayValue"] = {}
        body["realms"]["mapValue"]["fields"][realm]["arrayValue"]["values"] = []
        for org_id in new_realms[realm]:
            body["realms"]["mapValue"]["fields"][realm]["arrayValue"]["values"].append(
                {"stringValue": org_id}
            )
    return body

def create_firestore_password_request_body(password):
    body = {
        "password": {
            "stringValue": password
        }
    }
    return body

def create_firestore_request_body(realms, password):
    body = {
        "fields": {
            "realms": realms["realms"],
            "password": password["password"]
        }
    }
    return body

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
