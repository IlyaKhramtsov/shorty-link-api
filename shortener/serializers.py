from rest_framework import serializers

from .models import Shortener


class ShortenerSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Shortener
        fields = '__all__'

    def get_short_url(self, obj):
        request = self.context['request']
        hostname = request.META['HTTP_HOST']
        return f'{request.scheme}://{hostname}/{obj.short_id}'
