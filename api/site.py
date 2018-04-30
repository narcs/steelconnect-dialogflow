import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class SiteAPI:

    def __init__(self, auth, base_config_url, org_config_url):
        self.auth = auth
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url

    def list_sites(self):
        url = self.org_config_url + "sites"
        return requests.get(url, auth=self.auth)

    def get_site(self, site_id):
        url = self.base_config_url + "site/" + site_id
        return requests.get(url, auth=self.auth)

    def create_site(self, name, city, country_code):
        url = self.org_config_url + "sites"
        data = {
            "name": name,
            "longname": name,
            "city": city,
            "country": country_code
            }
        data = format_data(data)
        return requests.post(url, data=data, auth=self.auth)