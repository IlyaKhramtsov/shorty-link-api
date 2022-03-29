from django.test import TestCase
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework.test import APIRequestFactory

from shortener.models import Shortener
from shortener.serializers import ShortenerSerializer


class ShortenerSerializerTestCase(TestCase):
    def test_contains_expected_data(self):
        shortener = Shortener.objects.create(
            link='https://www.example.com/test-long-string',
            short_id='custom-id'
        )
        request_factory = APIRequestFactory()
        request = request_factory.post(reverse('shortener-detail', args=(shortener.id,)), HTTP_HOST='testserver')
        data = ShortenerSerializer(shortener, context={"request": request}).data
        data["created"] = parse_datetime(data["created"])
        expected_data = {
            'id': shortener.id,
            'short_url': 'http://testserver/custom-id',
            'link': 'https://www.example.com/test-long-string',
            'short_id': 'custom-id',
            'created': shortener.created
        }
        self.assertEqual(expected_data, data)
