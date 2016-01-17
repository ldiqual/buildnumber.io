import json
import datetime
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
        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_create_second_build(self):

        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        response1 = self.client.post(url, {})
        response2 = self.client.post(url, {})

        data2 = json.loads(response2.content)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data2.get('buildNumber'), 2)

    def test_create_build_with_data(self):
        
        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {
            'head': '05ef53a6',
            'from': 'circle-ci'
        })

        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('head'), '05ef53a6')
        self.assertEqual(data.get('from'), 'circle-ci')

    def test_get_last_build(self):
        
        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})
        
        url = '/api/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_ensure_no_last_build_with_new_account(self):

        url = '/api/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_build_for_different_packages(self):

        url1 = '/api/com.example.app1/builds?token=%s' % (self.api_key.key,)
        url2 = '/api/com.example.app2/builds?token=%s' % (self.api_key.key,)

        response1 = self.client.post(url1, {})
        response2 = self.client.post(url2, {})

        data1 = json.loads(response1.content)
        data2 = json.loads(response2.content)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data1.get('buildNumber'), 1)
        self.assertEqual(data2.get('buildNumber'), 1)

    def test_reserved_fields(self):

        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)

        for field_name in ['buildNumber', 'id', 'pk', 'extra', 'created_at', 'createdAt']:
            response = self.client.post(url, {field_name: 'value'})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_on_big_payload(self):

        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        payload = {"bigField": "1" * 1025}
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_last_build_relies_on_build_number(self):

        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        url = '/api/com.example.app/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        last_build = Build.objects.get(build_number=1)
        last_build.created_at = timezone.now() - datetime.timedelta(hours = 1)
        last_build.save()

        url = '/api/com.example.app/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 2)

    def test_fails_when_unauthenticated(self):
        url = '/api/com.example.app/builds'
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fails_with_invalid_api_token(self):
        url = '/api/com.example.app/builds?token=3cd7a0db76ff9dca48979e24c39b408c'
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
