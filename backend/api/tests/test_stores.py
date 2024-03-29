from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json

class TestStores(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.stores_register_url = reverse("stores_register")
        self.stores_login_url = reverse("stores_login")
        self.stores_account_url = reverse("stores_account")
        self.stores_pack_url = reverse("stores_packs")

    def test_stores_create_pack_success(self):
        raw_data = {
            "phone": "1234567",
            "name": "Domihoes",
            "image": "",
            "username": "domihoes",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.stores_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data = {
            "name": "comidasobra",
            "description": "Un perro, una hamburguesa",
            "stock": 2,
            "price": 5,
            "type": "random"
        }
        self.client.credentials(session=token["token"])
        response = self.client.put(self.stores_pack_url,format='json',data=raw_data,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

    def test_stores_register_login_account_success(self):
        raw_data = {
            "phone": "1234567",
            "name": "Domihoes",
            "image": "",
            "username": "domihoes",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.stores_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data = {
            "phone": "1234567",
            "name": "Dominoes",
            "image": "",
            "password": "1234567890",
            "address": "Calle 13"
        }
        self.client.credentials(session=token["token"])
        response = self.client.patch(self.stores_account_url,format='json',data=raw_data,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

    def test_stores_register_login_bad_username(self):
            raw_data = {
                "phone": "1234567",
                "name": "Domihoes",
                "image": "",
                "username": "domihoes",
                "password": "12345",
                "address": "Calle 13"
            }
            response = self.client.put(self.stores_register_url,format='json',data=raw_data)

            self.assertEquals(response.status_code,200)

            raw_data = {
                "username": "dominoes",
                "password": "12345",
            }
            response = self.client.post(self.stores_login_url,format='json',data=raw_data)
            self.assertEquals(response.status_code,401)

    def test_stores_register_login_bad_password(self):
            raw_data = {
                "phone": "1234567",
                "name": "Domihoes",
                "image": "",
                "username": "domihoes",
                "password": "12345",
                "address": "Calle 13"
            }
            response = self.client.put(self.stores_register_url,format='json',data=raw_data)

            self.assertEquals(response.status_code,200)

            raw_data = {
                "username": "domihoes",
                "password": "123456",
            }
            response = self.client.post(self.stores_login_url,format='json',data=raw_data)
            self.assertEquals(response.status_code,401)

    def test_stores_register_login_account_bad_token(self):
        raw_data = {
            "phone": "1234567",
            "name": "Domihoes",
            "image": "",
            "username": "domihoes",
            "password": "12345",
            "address": "Calle 13"
        }
        response = self.client.put(self.stores_register_url,format='json',data=raw_data)

        self.assertEquals(response.status_code,200)

        raw_data = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data)
        self.assertEquals(response.status_code,200)

        token = "bad_token"
        raw_data = {
            "phone": "1234567",
            "name": "Dominoes",
            "image": "",
            "password": "1234567890",
            "address": "Calle 13"
        }
        self.client.credentials(session=token)
        response = self.client.patch(self.stores_account_url,format='json',data=raw_data,HTTP_session=token)
        self.assertEquals(response.status_code,401)