import json
import datetime
import base64

from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import *

class BuildWithVersionTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        account = Account()
        account.save()
        self.account = account

        api_key = ApiKey(account = account)
        api_key.save()
        self.api_key = api_key
        
    def test_create_first_build(self):
        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {})
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_create_second_build(self):

        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        response1 = self.client.post(url, {})
        response2 = self.client.post(url, {})

        data2 = json.loads(response2.content)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data2.get('buildNumber'), 2)

    def test_create_build_with_data(self):
        
        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        response = self.client.post(url, {
            'head': '05ef53a6',
            'from': 'circle-ci'
        })

        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('head'), '05ef53a6')
        self.assertEqual(data.get('from'), 'circle-ci')

    def test_get_last_build(self):
        
        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})
        
        url = '/com.example.app/1.0/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 1)

    def test_ensure_no_last_build_with_new_account(self):

        url = '/com.example.app/1.0/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_build_for_different_packages(self):

        url1 = '/com.example.app1/1.0/builds?token=%s' % (self.api_key.key,)
        url2 = '/com.example.app2/1.0/builds?token=%s' % (self.api_key.key,)

        response1 = self.client.post(url1, {})
        response2 = self.client.post(url2, {})

        data1 = json.loads(response1.content)
        data2 = json.loads(response2.content)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data1.get('buildNumber'), 1)
        self.assertEqual(data2.get('buildNumber'), 1)

    def test_create_build_for_different_package_versions(self):

        # Mix builds with and without versions, make sure nothing conflicts
        url1 = '/com.example.app/builds?token=%s' % (self.api_key.key,)
        url2 = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        url3 = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        url4 = '/com.example.app/2.0/builds?token=%s' % (self.api_key.key,)
        url5 = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        url6 = '/com.example.app/2.0/builds?token=%s' % (self.api_key.key,)
        url7 = '/com.example.app/builds?token=%s' % (self.api_key.key,)

        response1 = self.client.post(url1, {})
        response2 = self.client.post(url2, {})
        response3 = self.client.post(url3, {})
        response4 = self.client.post(url4, {})
        response5 = self.client.post(url5, {})
        response6 = self.client.post(url6, {})
        response7 = self.client.post(url7, {})

        data1 = json.loads(response1.content)
        data2 = json.loads(response2.content)
        data3 = json.loads(response3.content)
        data4 = json.loads(response4.content)
        data5 = json.loads(response5.content)
        data6 = json.loads(response6.content)
        data7 = json.loads(response7.content)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response6.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response7.status_code, status.HTTP_201_CREATED)

        self.assertEqual(data1.get('buildNumber'), 1)
        self.assertEqual(data2.get('buildNumber'), 1)
        self.assertEqual(data3.get('buildNumber'), 2)
        self.assertEqual(data4.get('buildNumber'), 1)
        self.assertEqual(data5.get('buildNumber'), 3)
        self.assertEqual(data6.get('buildNumber'), 2)
        self.assertEqual(data7.get('buildNumber'), 2)

    def test_last_build_relies_on_build_number(self):

        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        url = '/com.example.app/1.0/builds?token=%s' % (self.api_key.key,)
        self.client.post(url, {})

        last_build = Build.objects.get(build_number=1)
        last_build.created_at = timezone.now() - datetime.timedelta(hours = 1)
        last_build.save()

        url = '/com.example.app/1.0/builds/last?token=%s' % (self.api_key.key,)
        response = self.client.get(url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('buildNumber'), 2)
