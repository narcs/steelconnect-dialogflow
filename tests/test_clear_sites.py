import unittest
from mock import patch, MagicMock

import requests
import app

from flask import json
from samples.create_site import *
from api.api_auth import SteelConnectAPI


# class MockResponse(Mock):
#     def __init__(self, json_data, status_code):
#         super().__init__()
#         # self.
#         self.status_code = status_code
#         self.json_data = json_data
#
#     def json(self):
#         return self.json_data


""" This doesn't test 'Clear Sites' at all"""

# class TestClearSites(unittest.TestCase):
#     def setUp(self):
#         self.app = app.app.test_client()
#
#     @patch('requests.post')
#     def test_clear_success(self):
#         mock_api = MagicMock()
#         mock_api.create_site.return_value = MagicMock(spec=requests.Response, status_code=200)
#         result = app.create_site(mock_api, finland_helsinki_parameters)
#         self.assertTrue(mock_api.create_site.called)
#         self.assertEqual(result)
#         result = app.clear_sites(mock_api)
#         #self.assertEqual(, result)

