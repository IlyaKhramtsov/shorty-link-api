from rest_framework import serializers

from .models import Shortener
from .utils import is_success_url


class ShortenerSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Shortener
        fields = '__all__'

    def get_short_url(self, obj):
        request = self.context['request']
        hostname = request.META['HTTP_HOST']
        return f'{request.scheme}://{hostname}/{obj.short_id}'

    def validate(self, data):
        """Check if the link exists."""
        url = data['link']
        if not is_success_url(url):
            raise serializers.ValidationError({"link": "this link doesn't exist"})
        return data
