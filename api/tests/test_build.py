import json
import datetime
import base64

from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import *

class BuildTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        account = Account()
        account.save()
        self.account = account

        api_key = ApiKey(account = account)
        api_key.save()
        self.api_key = api_key
        
    def test_create_first_build(self):
        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_create_second_build(self):

        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        response1 = self.client.post(url, {})
        response2 = self.client.post(url, {})

        data2 = json.loads(response2.content)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data2.get('buildNumber'), 2)

    def test_create_build_with_data(self):
        
        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {
            'head': '05ef53a6',
            'from': 'circle-ci'
        })

        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('head'), '05ef53a6')
        self.assertEqual(data.get('from'), 'circle-ci')

    def test_get_last_build(self):
        
        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})
        
        url = '/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_ensure_no_last_build_with_new_account(self):

        url = '/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_build_for_different_packages(self):

        url1 = '/com.example.app1/builds?token=%s' % (self.api_key.key,)
        url2 = '/com.example.app2/builds?token=%s' % (self.api_key.key,)

        response1 = self.client.post(url1, {})
        response2 = self.client.post(url2, {})

        data1 = json.loads(response1.content)
        data2 = json.loads(response2.content)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data1.get('buildNumber'), 1)
        self.assertEqual(data2.get('buildNumber'), 1)

    def test_reserved_fields(self):

        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)

        for field_name in ['buildNumber', 'id', 'pk', 'extra', 'created_at', 'createdAt']:
            response = self.client.post(url, {field_name: 'value'})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_on_big_payload(self):

        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        payload = {"bigField": "1" * 1025}
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_last_build_relies_on_build_number(self):

        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        url = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        last_build = Build.objects.get(build_number=1)
        last_build.created_at = timezone.now() - datetime.timedelta(hours = 1)
        last_build.save()

        url = '/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 2)

    def test_fails_when_unauthenticated(self):
        url = '/com.example.app/builds'
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fails_with_invalid_api_token(self):
        url = '/com.example.app/builds?token=3cd7a0db76ff9dca48979e24c39b408c'
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_package_is_unique_to_account(self):

        account1 = Account()
        account1.save()
        api_key1 = ApiKey(account = account1)
        api_key1.save()

        account2 = Account()
        account2.save()
        api_key2 = ApiKey(account = account2)
        api_key2.save()

        # Create a build with first account
        url = '/com.example.app/builds?token=%s' % (api_key1.key, )
        response = self.client.post(url, {})
        data = json.loads(response.content)
        self.assertEqual(data.get('buildNumber'), 1)

        # Fetch last (and first) build with account #1
        url = '/com.example.app/builds/last?token=%s' % (api_key1.key, )
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data.get('buildNumber'), 1)

        # Fetch build #1 with account #1
        url = '/com.example.app/builds/1?token=%s' % (api_key1.key, )
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data.get('buildNumber'), 1)

        # Make sure both steps above fail when authenticating with account #2
        # and using the same package name
        url = '/com.example.app/builds/last?token=%s' % (api_key2.key, )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/com.example.app/builds/1?token=%s' % (api_key2.key, )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auth_with_http_basic(self):
        url = '/com.example.app/builds'
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('%s:' % (self.api_key.key,)),
        }
        response = self.client.post(url, {}, **auth_headers)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('buildNumber'), 1)
