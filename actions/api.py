import logging

import requests
from requests.auth import HTTPBasicAuth
import requests_toolbelt.adapters.appengine

from flask import json

requests_toolbelt.adapters.appengine.monkeypatch()


class SteelConnectAPI:

    api_url = "https://{}/api/scm.config/1.0/"

    def __init__(self, username, password, base_url, org_id):
        self.auth = HTTPBasicAuth(username, password)
        self.base_url = base_url
        self.org_id = org_id

    @staticmethod
    def format_data(data):
        return json.dumps(data, indent=4)

    @staticmethod
    def find_context_by_name(contexts, name):
        for context in contexts:
            if context["name"] == name:
                return context
        else:
            return None

    @staticmethod
    def find_contexts_by_name(contexts, name):
        context_list = []
        for context in contexts:
            if context["name"] == name:
                context_list.append(context)
        return context_list


    def bare_url(self):
        return SteelConnectAPI.api_url.format(self.base_url)

    def org_url(self):
        return self.bare_url() + "org/{}/".format(self.org_id)

    def list_sites(self):
        url = self.org_url() + "sites"
        return requests.get(url, auth=self.auth)

    def list_wans(self):
        url = self.org_url() + "wans"
        return requests.get(url, auth=self.auth)

    def list_zones(self):
        url = self.org_url() + "zones"
        return requests.get(url, auth=self.auth)

    def list_nodes(self):
        url = self.org_url() + "nodes"
        return requests.get(url, auth=self.auth)

    def create_site(self, name, city, country_code):
        url = self.org_url() + "sites"
        data = {"name": name, "longname": name, "city": city, "country": country_code}
        data = self.format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def create_uplink(self, site, uplink, wan):
        url = self.org_url() + "uplinks"
        data = {
            "id": "",
            "site": site,
            "wan": wan,
            "org": self.org_id,
            "name": uplink,
        }
        # post uplink
        data = self.format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def create_wan(self, name):
        url = self.org_url() + "wans"
        data = {
            "name": name,
            "longname": name
        }
        data = self.format_data(data)
        return requests.post(url, data=data, auth=self.auth)
    
    def update_wan(self, wan_id, new_data):
        url = self.bare_url() + "wan/" + wan_id
        data = self.format_data(new_data)
        return requests.put(url, data=data, auth=self.auth)

    def delete_wan(self, wan_id):
        url = self.bare_url() + "wan/" + wan_id
        data = {}
        data = self.format_data(data)
        return requests.delete(url, data=data, auth=self.auth)

    def create_zone(self, name, site):
        url = self.org_url() + "zones"
        data = {
            "id": "",
            "name": name,
            "site": site
        }
        data = self.format_data(data)
        return requests.post(url, data=data, auth=self.auth)

    def create_appliance(self, model, site):
        url = self.org_url() + "node/virtual/register"
        data = {
            "site": site,
            "model": model
        }
        data = self.format_data(data)
        return requests.post(url, data=data, auth=self.auth)