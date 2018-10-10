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
    def get_uplink_info(self):
        url = self.base_reporting_url + 'uplinks'
        return requests.get(url, auth=self.auth)

    def set_uplink_list(self, uplink_list):
        self.uplinks = uplink_list
    
    def get_uplink_list(self):
        return self.uplinks

    def format_uplink_information(self, uplink_info):
        information = []
        #*(text)* is for bolding of text in the slack integration, which uses a markdown notation
        information.append('*Uplink ID:* {}\n'.format(uplink_info["id"]))
        information.append('*Uplink Name:* {}\n'.format(uplink_info["name"]))
        information.append('*Dead Interval:* {}\n'.format(uplink_info["dead_interval"]))        
        information.append('*Priority:* {}\n'.format(uplink_info["priority"]))
        information.append('*Site Link Priority:* {}\n'.format(uplink_info["sitelink_prio"]))
        information.append('*Up Time:* {}\n'.format(uplink_info["uptime"]))#
        information.append('*State:* {}\n'.format(uplink_info["state"]))
        information.append('*WAN:* {}\n'.format(uplink_info["wan"]))
        information.append('*Appliance:* {}\n'.format(uplink_info["node"]))#
        information.append('*Type:* {}\n'.format(uplink_info["type"]))
        information.append('*IP Address:* {}\n'.format(uplink_info["v4ip"]))#
        information.append('*Hello Interval:* {}\n'.format(uplink_info["hello_interval"]))
        information.append('*Cost:* {}\n'.format(uplink_info["cost"]))
        information.append('*Neighbour Hold Time:* {}\n'.format(uplink_info["bgp_neigh_hold_time"]))
        information.append('*Neighbour Keep Alive Time:* {}\n'.format(uplink_info["bgp_neigh_keepalive_time"]))
        information.append('*Inbound Units:* {}\n'.format(uplink_info["qos_inbound_units"]))
        information.append('*Outbound Units:* {}\n'.format(uplink_info["qos_outbound_units"]))
        return information
