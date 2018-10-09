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

    def rename_site(self, site_id, short_name, long_name, city, country_code):
        url = self.base_config_url + "site/" + site_id
        data = {
            "name": short_name,
            "longname": long_name,
            "city": city,
            "country": country_code
        }
        data = format_data(data)
        return requests.put(url, data=data, auth=self.auth)

    def delete_site(self, site_id):
        url = self.base_config_url + "site/" + site_id
        data = {}
        data = format_data(data)
        return requests.delete(url, data=data, auth=self.auth)

    def format_site_info(self, site_info):
        information = []
        information.append("Site ID: " + str(site_info["id"]) + "\n")
        information.append("Name: " + str(site_info["name"]) + "\n")
        information.append("Organisation: " + str(site_info["org"]) + "\n")
        information.append("City: " + str(site_info["city"])+ "\n")
        information.append("Country: " + str(site_info["country"]) + "\n")
        information.append("Uplinks: " + str(site_info["uplinks"]) + "\n")
        return information