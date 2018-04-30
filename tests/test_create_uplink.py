import unittest
from mock import patch, MagicMock

import requests
import app

from flask import json
from samples.create_uplink import *
from api import SteelConnectAPI

## The calls to the SteelConnect API need to be mocked - See Trello card

class TestCreateUplinks(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_melbourne_shop_success(self):
        mock_api = MagicMock()
        mock_api.create_uplink = MagicMock(name="create_uplink")
        mock_api.create_uplink.return_value = MagicMock(spec=requests.Response, status_code=200)
        mock_api.create_uplink.return_value.json.return_value = melbourne_shop_success_speech_response
        result = app.create_uplink(mock_api, melbourne_shop_parameters)
        self.assertTrue(mock_api.create_uplink.called)
        self.assertEqual(melbourne_shop_success_speech_response, result)

    def test_tonny_branch_invalid_site_400(self):
        mock_api = MagicMock()
        mock_api.create_uplink = MagicMock(name="create_uplink")
        mock_api.create_uplink.return_value = MagicMock(spec=requests.Response, status_code=400)
        mock_api.create_uplink.return_value.json.return_value = tonny_branch_invalid_site_400_api_response
        result = app.create_uplink(mock_api, tonny_branch_parameters)
        self.assertTrue(mock_api.create_uplink.called)
        self.assertEqual(tonny_branch_invalid_site_400_speech_response, result)

    def test_hahawan_invalid_wan_400(self):
        mock_api = MagicMock()
        mock_api.create_uplink = MagicMock(name="create_uplink")
        mock_api.create_uplink.return_value = MagicMock(spec=requests.Response, status_code=400)
        mock_api.create_uplink.return_value.json.return_value = hahawan_invalid_wan_400_api_response
        result = app.create_uplink(mock_api, hahawan_parameters)
        self.assertTrue(mock_api.create_uplink.called)
        self.assertEqual(hahawan_invalid_wan_400_speech_response, result)

    def test_melbourne_shop_500(self):
        mock_api =  MagicMock()
        mock_api.create_uplink = MagicMock(name="create_uplink")
        mock_api.create_uplink.return_value = MagicMock(spec=requests.Response, status_code=500)
        mock_api.create_uplink.return_value.json.return_value = melbourne_shop_500_api_response
        result = app.create_uplink(mock_api, melbourne_shop_parameters)
        self.assertTrue(mock_api.create_uplink.called)
        self.assertEqual(melbourne_shop_500_speech_response, result)

    def test_melbourne_shop_404(self):
        mock_api = MagicMock()
        mock_api.create_uplink = MagicMock(name="create_uplink")
        mock_api.create_uplink.return_value = MagicMock(spec=requests.Response, status_code=404)
        mock_api.create_uplink.return_value.json.return_value = melbourne_shop_404_speech_response
        result = app.create_uplink(mock_api, melbourne_shop_parameters)
        self.assertTrue(mock_api.create_uplink.called)
        self.assertEqual(melbourne_shop_404_speech_response, result)
