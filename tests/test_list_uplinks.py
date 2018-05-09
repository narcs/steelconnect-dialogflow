import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from mock import patch, MagicMock
from flask import json

import requests

from actions.uplink import list_uplinks
from samples.list_uplinks import *


class TestListSite(unittest.TestCase):
    def setUp(self):
        pass

    def test_success_1_uplink(self):
        mock_api = MagicMock()
        mock_api.uplink.list_uplinks.return_value = MagicMock(spec=requests.Response, status_code=200)
        mock_api.uplink.list_uplinks.return_value.json.return_value = case1_success_1_uplinks_return

        mock_api.site.get_site = site_return

        mock_api.wan.get_wan = wan_return

        result = list_uplinks(mock_api, case1_basic_request, {})

        self.assertTrue(mock_api.uplink.list_uplinks.called)
        self.assertEqual(case1_success_1_uplinks, result)

if __name__ == "__main__":
    unittest.main()