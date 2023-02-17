from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import storesRegister, storesLogin, storesAccount, clientsRegister, clientsLogin, clientsAccount

class TestUrls(SimpleTestCase):

    def test_stores_register_resolves(self):
        url = reverse("stores_register")
        self.assertEquals(resolve(url).func,storesRegister)

    def test_stores_login_resolves(self):
        url = reverse("stores_login")
        self.assertEquals(resolve(url).func,storesLogin)

    def test_stores_account_resolves(self):
        url = reverse("stores_account")
        self.assertEquals(resolve(url).func,storesAccount)

    def test_clients_register_resolves(self):
        url = reverse("clients_register")
        self.assertEquals(resolve(url).func,clientsRegister)

    def test_clients_login_resolves(self):
        url = reverse("clients_login")
        self.assertEquals(resolve(url).func,clientsLogin)

    def test_clients_account_resolves(self):
        url = reverse("clients_account")
        self.assertEquals(resolve(url).func,clientsAccount)