import json
import datetime
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import *

class AccountTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        account = Account()
        account.save()
        self.account = account

        api_key = ApiKey(account = account)
        api_key.save()
        self.api_key = api_key

    def test_create_account(self):
        url = '/accounts'
        response = self.client.post(url, {'email': 'me@example.com'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        account_email = AccountEmail.objects.get(email='me@example.com')
        api_key = account_email.account.api_keys.last()
        self.assertTrue(len(api_key.key) == 32)

    def test_ensure_creating_two_accounts_with_same_email_fails(self):
        url = '/accounts'
        response1 = self.client.post(url, {'email': 'me@example.com'})
        response2 = self.client.post(url, {'email': 'me@example.com'})

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        