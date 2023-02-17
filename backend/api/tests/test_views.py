from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Stores, Clients
import json

class TestStores(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.echo_url = reverse('echo')
        self.stores_register_url = reverse("stores_register")
        self.stores_login_url = reverse("stores_login")

    def test_echo_GET(self):
        response = self.client.get(self.echo_url)
        self.assertEquals(response.status_code, 200)

    def test_stores_register_login_success(self):
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
        
    def test_stores_register_login_bad_credentials(self):
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
                "password": "123456",
            }
            response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
            self.assertEquals(response.status_code,401)