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

#Actions for sites 
from actions.create_site import create_site
from actions.delete_site import delete_site
from actions.get_site_info import get_site_info
from actions.list_sites import list_sites
from actions.rename_site import rename_site

#Actions for WANs
from actions.create_wan import create_wan
from actions.delete_wan import delete_wan
from actions.get_wan import get_wan
from actions.list_wans import list_wans
from actions.rename_wan import rename_wan

#untested actions that could be useful in the future
from actions.create_zone import create_zone
from actions.add_site_to_wan import add_site_to_wan
from actions.add_sites_to_wan import add_sites_to_wan
from actions.clear_sites import clear_sites

#Actions for appliances
from actions.create_appliance import create_appliance
from actions.delete_appliance import delete_appliance
from actions.delete_appliance_followup import delete_appliance_followup
from actions.get_appliances_report import get_appliances_report
from actions.get_appliance_info import get_appliance_info
from actions.get_appliance_info_followup import get_appliance_info_followup
from actions.list_appliances import list_appliances

#Actions for uplinks
from actions.create_uplink import create_uplink
from actions.delete_uplink import delete_uplink
from actions.delete_uplink_followup import delete_uplink_followup
from actions.get_uplink_info import get_uplink_info
from actions.get_uplinks_report import get_uplinks_report
from actions.get_uplink_info_followup import get_uplink_info_followup
from actions.list_uplinks import list_uplinks

#Actions for sitelinks
from actions.get_sitelinks_report import get_sitelinks_report

app = Flask(__name__)
app.Debug = True

# Enable error logging through app engine logging.
# https://stackoverflow.com/a/42547090
@app.before_request
def enable_local_error_handling():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
FIRESTORE_API = "https://firestore.googleapis.com/v1beta1/projects/{}/databases/(default)/documents".format(firestore_project_id)
COLLECTION = "Accounts"

# CSS notification category classes
PRIMARY = "is-primary"
LINK = "is_link"
INFO = "is-info"
SUCCESS = "is-success"
WARNING = "is-warning"
DANGER = "is-danger"

app.config["SC_API"] = None

# Register actions.
# 
# Actions are functions with the signature `(api_auth, parameters, contexts) -> response_string`
actions = {}

def register_action(name, func):
    actions[name] = func

def get_appliance_info_followup_custom(api_auth, parameters, contexts):
    return get_appliance_info_followup(api_auth, contexts[0]["parameters"], contexts)

def delete_appliance_followup_custom(api_auth, parameters, contexts):
    return delete_appliance_followup(api_auth, contexts[0]["parameters"], contexts)

def get_uplink_info_followup_custom(api_auth, parameters, contexts):
    return get_uplink_info_followup(api_auth, contexts[0]["parameters"], contexts)

#Actions for sites
register_action("CreateSite", create_site)
register_action("DeleteSite", delete_site)
register_action("GetSiteInfo", get_site_info)
register_action("ListSites", list_sites)
register_action("RenameSite", rename_site)

#Actions for uplinks
register_action("CreateUplink", create_uplink)
register_action("DeleteUplink", delete_uplink) 
register_action("DeleteUplink.DeleteUplink-custom", delete_uplink_followup) 
register_action("GetUplinkInfo", get_uplink_info)
register_action("GetUplinkInfo.GetUplinkInfo-custom", get_uplink_info_followup_custom)
register_action("GetUplinksReport", get_uplinks_report)
register_action("ListUplinks", list_uplinks)

#Action for WANs
register_action("CreateWAN", create_wan)
register_action("DeleteWAN", delete_wan)
register_action("GetWAN", get_wan)
register_action("ListWANs", list_wans)
register_action("RenameWAN", rename_wan)

#Actions for Appliances
register_action("CreateAppliance", create_appliance)
register_action("DeleteAppliance", delete_appliance)
register_action("DeleteAppliance.DeleteAppliance-custom", delete_appliance_followup_custom)
register_action("GetApplianceInfo", get_appliance_info)
register_action("GetApplianceInfo.GetApplianceInfo-custom", get_appliance_info_followup_custom)
register_action("GetAppliancesReport", get_appliances_report)
register_action("ListAppliances", list_appliances)

#Actions for sitelinks
register_action("GetSitelinksReport", get_sitelinks_report)

#Untested actions but could be useful in the future
register_action("ClearSites", clear_sites)
register_action("AddSiteToWAN", add_site_to_wan)
register_action("AddSitesToWAN", add_sites_to_wan)
register_action("CreateZone", create_zone)

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
        response = "Not authenticated. Login at: {}authenticate".format(request.host_url)
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
    """
    Validate username and password from Firestore Database
    :param firestore_collection_api: REST API URL for Firestore Database collection
    :type firestore_collection_api: string 
    :param username: SteelConnect username 
    :type username: string 
    :param password: SteelConnect password
    :type password:string 
    :return: Dict object of SteelConnect Account details from Firestore Database, or string
             if error
    :rtype: Dict, or string
    """
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

def valid_passwords_match(password_1, password_2, field):
    """
    Check whether 'password_1' and 'password_2' match
    :param password_1: password 
    :type password_1: string 
    :param password_2: password 
    :type password_2: string 
    :param field: Type of password field (e.g. 'New password')
    :type field: string 
    :return: True if passwords match, string error message otherwise
    :rtype: Boolean, or string
    """
    if password_1 == "":
        if field:
            return "{} password cannot be blank".format(field)
        else:
            return "Password cannot be blank"
    elif password_1 == password_2:
        return True
    else:
        return "Password confirm does not match"

def create_notification(category, message):
    """
    Create object to pass to Jinja2 template to create notifications
    :param category: CSS category styling class
    :type category: string 
    :param message: notification message
    :type message: string 
    :return: Dict object suitable to create notification in Jinja2 template
    :rtype: Dict
    """
    notification = {
        "category": category,
        "message": message,
    }
    return notification

@app.route("/test")
def test():
    notification_1 = create_notification(DANGER, "hello")
    notification_2 = create_notification(SUCCESS, "hello")
    notifications = [notification_1, notification_2]
    return render_template("test.html", notifications=notifications)

@app.route("/authenticate", methods=["GET", "POST"])
def authenticate(title="Authentication", authenticated=None, notification=None):
    """
    Page to allow users to login and authenticate through Firestore Database:
    :return: HTML
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "":
            notification = create_notification(WARNING, "Username not entered")
            return render_template("authenticate.html", title=title, authenticated=authenticated, notification=notification)
        # Get data from Firestore
        data = validate_username_password(FIRESTORE_API + "/{}/".format(COLLECTION), username, password)
        if isinstance(data, str):
            notification = create_notification(DANGER, data)
            return render_template("authenticate.html", title=title, authenticated=authenticated, notification=notification)
        else:
            # Get realm
            realms = data["realms"]["mapValue"]["fields"]
            realm = realms.keys()[0] # Get first key TODO: allow users to choose realm
            # Get organisation id
            org_ids = realms[realm]["arrayValue"]["values"]
            org_id = org_ids[0]["stringValue"] # Get first org_id TODO: allow users to choose org_id
            app.config["SC_API"] = SteelConnectAPI(username, password, realm, org_id)
            authenticated = app.config["SC_API"]
            notification = create_notification(SUCCESS, "Successfully logged in as: {}".format(username))
            return render_template("authenticate.html", title=title, authenticated=authenticated, notification=notification)
    if app.config["SC_API"]:
        authenticated = app.config["SC_API"]
    return render_template("authenticate.html", title=title, authenticated=authenticated, notification=notification)

@app.route("/status")
def status():
    """
    Get server authentication status - whether anyone is currently logged in
    :return: Returns a json formatted response
    :rtype: json
    """
    if not app.config["SC_API"]:
        return format_response("Currently not authenticated. Login at: {}authenticate".format(request.host_url))
    else:
        return format_response("Logged in as: {}".format(app.config["SC_API"].auth.username))

@app.route("/logout")
def logout():
    """
    Logs out anyone currently authenticated and redirects to /authenticate
    """
    app.config["SC_API"] = None
    return redirect(url_for("authenticate"))

@app.route("/create", methods=["GET", "POST"])
def create(title="Create Account", notifications=None, notification=None):
    """
    Page to allow users to create a new account with fields:
        - Username
        - Password
        - Realm
        - Organisation I.d
    :return: HTML
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        realm = request.form["realm"]
        org_id = request.form["org_id"]
        notifications = []
        if username == "":
            notification = create_notification(WARNING, "Username not entered")
            notifications.append(notification)
        valid_passwords = valid_passwords_match(password, password_confirm, None)
        if isinstance(valid_passwords, str):
            notification = create_notification(DANGER, valid_passwords)
            notifications.append(notification)
        if realm == "":
            notification = create_notification(WARNING, "Realm not entered")
            notifications.append(notification)
        if org_id == "":
            notification = create_notification(WARNING, "Organisation Id not entered")
            notifications.append(notification)
        if len(notifications) > 0:
            return render_template("create.html", title=title, notifications=notifications)
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
            request_url = "{}{}{}{}".format(FIRESTORE_API, "/{}".format(COLLECTION), "?documentId=", document_id)
            res = requests.post(request_url, json=request_body)
            if res.status_code == 200:
                notification = create_notification(SUCCESS, "Successfully created account: {}".format(username))
                return render_template("create.html", title=title, notification=notification)
            elif res.status_code == 409:
                notification = create_notification(DANGER, "Account already exists: {}".format(username))
                return render_template("create.html", title=title, notification=notification)
            else:
                notification = create_notification(DANGER, "Error status code: {}".format(res.status_code))
                return render_template("create.html", title=title, notification=notification)

    return render_template("create.html", title=title, notification=notification)

@app.route("/change_password", methods=["GET", "POST"])
def change_password(title="Change Password", notifications=None, notification=None):
    """
    Page to allow users to change password
    :return: HTML
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_password = request.form["new_password"]
        new_password_confirm = request.form["new_password_confirm"]
        notifications = []
        if username == "":
            notification = create_notification(WARNING, "Username not entered")
            notifications.append(notification)
        valid_new_passwords = valid_passwords_match(new_password, new_password_confirm, "New")
        if isinstance(valid_new_passwords, str):
            notification = create_notification(DANGER, valid_new_passwords)
            notifications.append(notification)
        if len(notifications) > 0:
            return render_template("change_password.html", title=title, notifications=notifications)
        # Validate username and password
        data = validate_username_password(FIRESTORE_API + "/{}/".format(COLLECTION), username, password)
        if isinstance(data, str):
            notification = create_notification(DANGER, data)
            return render_template("change_password.html", title=title, notification=notification)
        else:
            # Update password
            res = requests.get(FIRESTORE_API + "/{}/".format(COLLECTION) + username)
            if res.status_code == 200:
                data = res.json()
                hashed_password = generate_password_hash(new_password)
                data["fields"]["password"]["stringValue"] = hashed_password 
                del data["name"]
                del data["createTime"]
                del data["updateTime"]
                res = requests.patch(FIRESTORE_API + "/{}/".format(COLLECTION) + username + "?currentDocument.exists=true", json=data)
                if res.status_code == 200:
                    notification = create_notification(SUCCESS, "Password successfully changed")
                    return render_template("change_password.html", title=title, notification=notification)
                else:
                    notification = create_notification(DANGER, "Error status code: {}".format(res.status_code))
                    return render_template("change_password.html", title=title, notification=notification)
    return render_template("change_password.html", title=title)

def create_firestore_realms_request_body(new_realms):
    """
    Create request body to insert fields 'realms' for REST API Firestore Database document 
    :param realms: object for 'realms' field suitable for REST API Firestore Database
    :type realms: Dict
    :return: Returns a Dict object suitable for a REST API Firestore request
    :rtype: Dict 
    """
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
    """
    Create request body to insert fields 'password' for REST API Firestore Database document 
    :param password: object for 'password' field suitable for REST API Firebase Database
    :type password: Dict
    :return: Returns a Dict object suitable for a REST API Firestore request
    :rtype: Dict 
    """
    body = {
        "password": {
            "stringValue": password
        }
    }
    return body

def create_firestore_request_body(realms, password):
    """
    Create request body to insert fields 'realms' and 'password' for REST API Firestore Database document 
    :param realms: object for 'realms' field suitable for REST API Firestore Database
    :type realms: Dict
    :param password: object for 'password' field suitable for REST API Firebase Database
    :type password: Dict
    :return: Returns a Dict object suitable for a REST API Firestore request
    :rtype: Dict 
    """
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
    # app.secret_key = 'H\xa9\xde\xe5\xd8\x19J\x01T\x17\x95\xbf~\xc4\xf1Q\x96ph?4;\xd8k'
    app.run(debug=True, port=8080, host='127.0.0.1')