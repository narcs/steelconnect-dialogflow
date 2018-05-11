import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class NodeAPI:

    def __init__(self, auth, base_config_url, org_config_url, base_reporting_url, org_reporting_url):
        self.auth = auth
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url
        self.base_reporting_url = base_reporting_url
        self.org_reporting_url = org_reporting_url

        # This variable stores information about multiple appliances on a site. 
        # Hesitant to put in, but it is currently the only way to 
        # transfer information from parameters between contexts
        # Use this for now, try to fix later as we get more used to dialogflow
        self.appliances = None          

    def list_appliances(self): 
        url = self.org_config_url + "nodes" 
        return requests.get(url, auth=self.auth) 

    def get_appliance_info(self, node_id):
        url = self.base_reporting_url + "node/" + node_id
        return requests.get(url, auth=self.auth)

    def create_appliance(self, site, model):
        url = self.org_config_url + "node/virtual/register"
        data = {
            "site": site,
            "model": model
        }
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def create_appliance_new(self, site, model):
        url = self.org_config_url + "node/virtual/register"
        data = {
            "site": site,
            "model": model
        }
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def delete_appliance(self, appliance_id):
        url = self.base_config_url + "node/" + appliance_id
        data = {}
        data = format_data(data)
        return requests.delete(url, data=data, auth=self.auth)

    def set_appliance_list(self, appliance_list):
        self.appliances = appliance_list

    def get_appliance_list(self):
        return self.appliances

    def format_appliance_information(self, appliance_info): #Prevent duplicated code in get_appliance_info and get_appliance_info_followup
        information = []
        information.append("Appliance ID: " + str(appliance_info["id"]) + "\n")         #Need to specify str(json[key]), otherwise it is unavailable in dialogflow
        information.append("Model: " + str(appliance_info["model"]) + "\n")
        information.append("Organisation: " + str(appliance_info["org"]) + "\n")
        information.append("Site: " + str(appliance_info["site"])+ "\n")
        information.append("Serial: " + str(appliance_info["serial"]) + "\n")
        information.append("Uptime: " + str(appliance_info["uptime"]) + "\n")
        information.append("CPU Load: " + str(appliance_info["cpu_load"]) + "\n")
        information.append("Mem Load" + str(appliance_info["mem_load"]) + "\n")
        information.append("State: " + str(appliance_info["state"]) + "\n")
        information.append("Last Online: " + str(appliance_info["last_online"]) + "\n")
        return information