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