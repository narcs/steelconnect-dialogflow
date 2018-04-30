import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class UplinkAPI:

    def __init__(self, auth, org_id, base_config_url, org_config_url, base_reporting_url, org_reporting_url):
        self.auth = auth
        self.org_id = org_id
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url
        self.base_reporting_url = base_reporting_url
        self.org_reporting_url = org_reporting_url

    def list_uplinks(self):
        url = self.org_config_url + "uplinks"
        return requests.get(url, auth=self.auth)

    def get_uplink(self, uplink_id):
        url = self.base_config_url + "uplink/" + uplink_id 
        return requests.get(url, auth=self.auth)

    def create_uplink(self, site, uplink, wan):
        url = self.org_config_url + "uplinks"
        data = {
            "id": "",
            "site": site,
            "wan": wan,
            "org": self.org_id,
            "name": uplink,
        }
        # post uplink
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)

