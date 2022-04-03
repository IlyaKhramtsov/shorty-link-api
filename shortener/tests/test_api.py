import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from shortener.models import Shortener


class ShortenerApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.link_1 = Shortener.objects.create(
            link='https://docs.djangoproject.com/en/4.0/',
            owner=self.user
        )
        self.link_2 = Shortener.objects.create(
            link='https://www.djangoproject.com/community/',
            short_id='custom-id',
            owner=self.user
        )

    def test_get(self):
        url = reverse('shortener-list')
        response = self.client.get(url, HTTP_HOST='testserver')
        expected_url = 'http://testserver/custom-id'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['short_url'], expected_url)

    def test_create(self):
        self.assertEqual(2, Shortener.objects.all().count())
        url = reverse('shortener-list')
        data = {
            'link': 'https://www.django-rest-framework.org/api-guide/testing/',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json', HTTP_HOST='testserver')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Shortener.objects.all().count())

    def test_update(self):
        url = reverse('shortener-detail', args=(self.link_2.id,))
        data = {
            "link": self.link_2.link,
            "short_id": 'changed-id',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_HOST='testserver')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.link_2.refresh_from_db()
        self.assertEqual('changed-id', self.link_2.short_id)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')
        url = reverse('shortener-detail', args=(self.link_2.id,))
        data = {
            "link": self.link_2.link,
            "short_id": 'changed-id',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_HOST='testserver')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.link_2.refresh_from_db()
        self.assertEqual('custom-id', self.link_2.short_id)

    def test_delete(self):
        self.assertEqual(2, Shortener.objects.all().count())
        url = reverse('shortener-detail', args=(self.link_2.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, HTTP_HOST='testserver')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Shortener.objects.all().count())

    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')
        url = reverse('shortener-detail', args=(self.link_2.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, HTTP_HOST='testserver')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(2, Shortener.objects.all().count())
