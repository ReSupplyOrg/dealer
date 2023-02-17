from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json

class TestClients(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.stores_register_url = reverse("stores_register")
        self.stores_login_url = reverse("stores_login")
        self.seach_stores_url = reverse("search_stores")

    def test_search_stores_success(self):
        raw_data = {
            "phone": "1234567",
            "name": "Domihoes",
            "username": "domihoes",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.stores_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data2 = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
        "name": "domi",
        "phone": "",
        "rating": 0,
        "address": "",
        "username": "",
        "page": 0
        }
        self.client.credentials(session=token["token"])
        response = self.client.post(self.seach_stores_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        