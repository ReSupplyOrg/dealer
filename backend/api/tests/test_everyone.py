from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json
import requests
from django.core.files.uploadedfile import SimpleUploadedFile

class TestClients(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.stores_register_url = reverse("stores_register")
        self.stores_login_url = reverse("stores_login")
        self.seach_stores_url = reverse("search_stores")
        self.stores_pack_url = reverse("stores_packs")
        #self.stores_pack_patch_url = reverse("stores_packs_id")
        self.search_orders_url = reverse("search_orders")
        self.search_packs_url = reverse("search_packs")

    def test_search_stores_success(self):
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

    def test_search_stores_no_arguments(self):
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

        raw_data2 = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
        "name": "tiendanoexistente",
        "phone": "",
        "rating": 0,
        "address": "",
        "username": "",
        "page": 0
        }
        self.client.credentials(session=token["token"])
        response = self.client.post(self.seach_stores_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.data,{"totalPages": 1,"items": []})

    def test_stores_create_pack_search_packs_orders_success(self):
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

        raw_data2 = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
            "name": "comidasobra",
            "description": "Un perro, una hamburguesa",
            "stock": 2,
            "price": 5,
            "type": "random"
        }
        self.client.credentials(session=token["token"])
        response = self.client.put(self.stores_pack_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        raw_data4 = {
            "name": "",
            "description": "",
            "owner": "",
            "stock": 2,
            "price": 5,
            "pack_type": "random",
            "page": 0
        }
        self.client.credentials(session=token["token"])
        response = self.client.post(self.search_packs_url,format='json',data=raw_data4,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        raw_data5 = {
            "client_uuid": "",
            "store_uuid": "",
            "pack_uuid": "",
            "payed_price": 5,
            "page": 0
        }
        self.client.credentials(session=token["token"])
        response = self.client.post(self.search_orders_url,format='json',data=raw_data5,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

    def test_stores_delete_pack_success(self):
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

        raw_data2 = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
            "name": "comidasobra",
            "description": "Un perro, una hamburguesa",
            "stock": 2,
            "price": 5,
            "type": "random"
        }
        self.client.credentials(session=token["token"])
        response = self.client.put(self.stores_pack_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        raw_data4 = {
            "name": "",
            "description": "",
            "owner": "",
            "stock": 2,
            "price": 5,
            "pack_type": "random",
            "page": 0
        }
        self.client.credentials(session=token["token"])
        response = self.client.post(self.search_packs_url,format='json',data=raw_data4,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)
        item = response.data["items"][0]
        uuid = item["uuid"]

        raw_data5 = {
            "name": "cambio",
            "description": "sizas",
            "stock": 0,
            "price": 0,
            "packType": "vegetales"
        }

        response = self.client.patch(f"/stores/packs/{uuid}",format='json',data=raw_data5,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        response = self.client.delete(f"/stores/packs/{uuid}",format='json',data=raw_data5,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)


    def test_packs_image_success(self):

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

        raw_data2 = {
            "username": "domihoes",
            "password": "12345",
        }
        response = self.client.post(self.stores_login_url,format='json',data=raw_data2)
        self.assertEquals(response.status_code,200)

        token = json.loads(response.content.decode('utf-8'))
        raw_data3 = {
            "name": "comidasobra",
            "description": "Un perro, una hamburguesa",
            "stock": 2,
            "price": 5,
            "type": "random"
        }
        self.client.credentials(session=token["token"])
        response = self.client.put(self.stores_pack_url,format='json',data=raw_data3,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)

        raw_data4 = {
            "name": "",
            "description": "",
            "owner": "",
            "stock": 2,
            "image": "",
            "price": 5,
            "pack_type": "random",
            "page": 0
        }
        response = self.client.post(self.search_packs_url,format='json',data=raw_data4,HTTP_session=token["token"])
        self.assertEquals(response.status_code,200)
        item = response.data["items"][0]
        uuid = item["uuid"]
        response = self.client.get(f"/images/pack/{uuid}",format='json',HTTP_session=token["token"])
        self.assertEquals(response.status_code,404)
        
    def test_stores_image_success(self):

        raw_data = {
            "phone": "1234567",
            "name": "Domihoes",
            "image_bytes": "",
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
        item = response.data["items"][0]
        uuid = item["uuid"]

        response = self.client.get(f"/images/stores/{uuid}",format='json',HTTP_session=token["token"])
        self.assertEquals(response.status_code,404)