import requests
import requests_toolbelt.adapters.appengine
from util import format_data
import logging

requests_toolbelt.adapters.appengine.monkeypatch()

class UplinkAPI:

    def __init__(self, auth, org_id, base_config_url, org_config_url, base_reporting_url, org_reporting_url):
        self.auth = auth
        self.org_id = org_id
        self.base_config_url = base_config_url
        self.org_config_url = org_config_url
        self.base_reporting_url = base_reporting_url
        self.org_reporting_url = org_reporting_url
        
        # This variable stores information about multiple uplinks on a site. 
        # Hesitant to put in, but it is currently the only way to 
        # transfer information from parameters between contexts
        # Use this for now, try to fix later as we get more used to dialogflow
        self.uplinks = None

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

    def delete_uplink(self, uplink_id):
        url = self.base_config_url + "uplink/" + uplink_id
        data = {}
        data = format_data(data)
        return requests.delete(url, data=data, auth=self.auth)

    # We need site_id to get the information about uplinks on a site
    def get_uplink_info(self, site_id):
        url = self.base_reporting_url + 'site/' + site_id + '/uplinks'
        return requests.get(url, auth=self.auth)

    def set_uplink_list(self, uplink_list):
        self.uplinks = uplink_list
    
    def get_uplink_list(self):
        return self.uplinks

    def format_uplink_information(self, uplink_info):
        information = []
        information.append('Uplink ID: ' + str(uplink_info["id"] + '\n'))
        information.append('Uplink Name: ' + str(uplink_info["name"] + '\n'))
        information.append('Dead Interval: ' + str(uplink_info["dead_interval"] + '\n'))
        information.append('Priority: ' + str(uplink_info["priority"] + '\n'))
        information.append('Site Link Priority: ' + str(uplink_info["sitelink_prio"]) + '\n')
        information.append('Up Time: ' + str(uplink_info["sitelink_prio"] + '\n'))
        information.append('State: ' + str(uplink_info["state"]) + '\n')
        information.append('WAN: ' + str(uplink_info["wan"]) + '\n')
        information.append('Appliance: ' + str(uplink_info["node"]) + '\n')
        information.append('Type: ' + str(uplink_info["type"]) + '\n')
        information.append('IP Address: ' + str(uplink_info["v4ip"]) + '\n')
        information.append('Hello Interval: ' + str(uplink_info["hello_interval"]) + '\n')
        information.append('Cost: ' + str(uplink_info["cost"]) + '\n')
        information.append('Neighbour Hold Time: ' + str(uplink_info["bgp_neigh_hold_time"]) + '\n')
        information.append('Neighbour Keep Alive Time: ' + str(uplink_info["state"]) + '\n')
        information.append('Inbound Units: ' + str(uplink_info["qos_inbound_units"]) + '\n')
        information.append('Outbound Units: ' + str(uplink_info["qos_outbound_units"]) + '\n')
        return str(information)

    def delete_uplink(self, uplink_id): 
        url = self.base_config_url + "uplink/" + uplink_id 
        data = {} 
        data = format_data(data) 
        return requests.delete(url, data=data, auth=self.auth) 
 