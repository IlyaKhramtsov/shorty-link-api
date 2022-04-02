import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import Shortener


class ShortenerApiTestCase(APITestCase):
    def setUp(self):
        self.link_1 = Shortener.objects.create(
            link='https://docs.djangoproject.com/en/4.0/'
        )
        self.link_2 = Shortener.objects.create(
            link='https://www.djangoproject.com/community/',
            short_id='custom-id'
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
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_HOST='testserver')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.link_2.refresh_from_db()
        self.assertEqual('changed-id', self.link_2.short_id)

    def test_delete(self):
        self.assertEqual(2, Shortener.objects.all().count())
        url = reverse('shortener-detail', args=(self.link_2.id,))
        response = self.client.delete(url, HTTP_HOST='testserver')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Shortener.objects.all().count())
