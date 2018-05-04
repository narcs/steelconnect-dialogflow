import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class WanAPI:

    def __init__(self, auth, base_config_url, org_config_url):
        self.auth = auth
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url

    def list_wans(self):
        url = self.org_config_url + "wans"
        return requests.get(url, auth=self.auth)

    def get_wan(self, wan_id):
        url = self.base_config_url + "wan/" + wan_id
        return requests.get(url, auth=self.auth)

    def create_wan(self, name):
        url = self.org_config_url + "wans"
        data = {
            "name": name,
            "longname": name
        }
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def update_wan(self, wan_id, new_data):
        url = self.base_config_url + "wan/" + wan_id
        data = format_data(new_data)
        return requests.put(url, data=data, auth=self.auth)

    def delete_wan(self, wan_id):
        url = self.base_config_url + "wan/" + wan_id
        data = {}
        data = format_data(data)
        return requests.delete(url, data=data, auth=self.auth)