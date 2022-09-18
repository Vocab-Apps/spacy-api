import unittest
import json
import tempfile
import datetime
import urllib.parse
import pprint
from app import app

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ApiTests, cls).setUpClass()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_languages(self):
        response = self.client.get('/language_list')
        data = json.loads(response.data)
        self.assertIn('en', data)

