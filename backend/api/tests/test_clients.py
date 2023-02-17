from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json

class TestClients(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.clients_register_url = reverse("clients_register")
        self.clients_login_url = reverse("clients_login")
        self.clients_account_url = reverse("clients_account")

    def test_clients_register_login_account_success(self):
        raw_data = {
            "phone": "1234567",
            "names": "juan perez",
            "username": "juanpaez12",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.clients_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data2 = {
            "username": "juanpaez12",
            "password": "12345",
        }
        response = self.client.post(self.clients_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
            "phone": "1234567",
            "names": "juan paez",
            "password": "1234567890",
            "address": "Calle 13"
        }
        self.client.credentials(session=token["token"])
        response = self.client.patch(self.clients_account_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

    def test_clients_register_login_bad_username(self):
        raw_data = {
            "phone": "1234567",
            "names": "juan perez",
            "username": "juanpaez12",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.clients_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data2 = {
            "username": "juanpaez13",
            "password": "12345",
        }
        response = self.client.post(self.clients_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,401)

    def test_clients_register_login_bad_password(self):
        raw_data = {
            "phone": "1234567",
            "names": "juan perez",
            "username": "juanpaez12",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.clients_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data2 = {
            "username": "juanpaez12",
            "password": "1234567",
        }
        response = self.client.post(self.clients_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,401)

    def test_clients_register_login_account_bad_token(self):
        raw_data3 = {
            "phone": "1234567",
            "names": "juan perez",
            "username": "juanpaez12",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.clients_register_url,format='json',data=raw_data3)

        self.assertEquals(response.status_code,200)

        raw_data2 = {
            "username": "juanpaez12",
            "password": "12345",
        }
        response = self.client.post(self.clients_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = "bad_token"
        raw_data3 = {
            "phone": "1234567",
            "names": "juanpaez123",
            "password": "1234567890",
            "address": "Calle 13"
        }
        self.client.credentials(session=token)
        response = self.client.patch(self.clients_account_url,format='json',data=raw_data3,HTTP_session=token)
        self.assertEquals(response.status_code,401)