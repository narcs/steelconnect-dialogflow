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
        information.append("Appliance ID: {}\n".format(appliance_info["id"]))         #Need to specify str(json[key]), otherwise it is unavailable in dialogflow
        information.append("Model: {}\n".format(appliance_info["model"]))        
        information.append("Organisation: {}\n".format(appliance_info["org"]))        
        information.append("Site: {}\n".format(appliance_info["site"]))        
        information.append("Serial: {}\n".format(appliance_info["serial"]))        
        information.append("Uptime: {}\n".format(appliance_info["uptime"]))        
        information.append("CPU Load: {}\n".format(appliance_info["cpu_load"]))        
        information.append("Mem Load: {}\n".format(appliance_info["mem_load"]))        
        information.append("State: {}\n".format(appliance_info["state"]))        
        information.append("Last Online: {}\n".format(appliance_info["last_online"]))        
        return information