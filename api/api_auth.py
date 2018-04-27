import logging
import requests
from requests.auth import HTTPBasicAuth
from flask import json
from site import SiteAPI
from wan import WanAPI
from zone import ZoneAPI
from node import NodeAPI
from uplink import UplinkAPI

class SteelConnectAPI:

    def __init__(self, username, password, base_url, org_id):
        self.auth = HTTPBasicAuth(username, password)
        self.base_url = base_url
        self.org_id = org_id

        self.base_config_url = "https://{}/api/scm.config/1.0/"
        self.api_base_config_url = self.base_config_url.format(self.base_url)
        self.org_config_url = "https://{}/api/scm.config/1.0/org/{}/"
        self.api_org_config_url = self.org_config_url.format(self.base_url, self.org_id)

        self.base_reporting_url = "https://{}/api/scm.reporting/1.0/"
        self.api_base_reporting_url = self.base_reporting_url.format(self.base_url)
        self.org_reporting_url = "https://{}/api/scm.reporting/1.0/org/{}/"
        self.api_org_reporting_url = self.org_reporting_url.format(self.base_url, self.org_id)

        self.api_site = SiteAPI(self.auth, self.base_config_url, self.org_config_url)
        self.api_wan = WanAPI(self.auth, self.base_config_url, self.org_config_url)
        self.api_zone = ZoneAPI(self.auth, self.base_config_url, self.org_config_url)
        self.api_node = NodeAPI(self.auth, self.base_config_url, self.org_config_url,
                                self.base_reporting_url, self.org_reporting_url)
        self.api_uplink = UplinkAPI(self.auth, self.org_id, self.base_config_url, self.org_config_url,
                                self.base_reporting_url, self.org_reporting_url)