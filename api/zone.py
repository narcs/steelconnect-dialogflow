import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class ZoneAPI:

    def __init__(self, auth, base_config_url, org_config_url):
        self.auth = auth
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url

    def list_zones(self):
        url = self.org_config_url + "zones"
        return requests.get(url, auth=self.auth)

    def create_zone(self, name, site):
        url = self.org_config_url + "zones"
        data = {
            "id": "",
            "name": name,
            "site": site
        }
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)
