import requests
import requests_toolbelt.adapters.appengine
from util import format_data

requests_toolbelt.adapters.appengine.monkeypatch()

class SitelinkAPI:
    def __init__(self, auth, base_reporting_url):
        self.auth = auth
        self.base_reporting_url = base_reporting_url

    def get_sitelinks(self, site_id):
        url = self.base_reporting_url + "site/{}/sitelinks".format(site_id)
        return requests.get(url, auth=self.auth)
