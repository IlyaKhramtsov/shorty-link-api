from rest_framework import viewsets

from .models import Shortener
from .serializers import ShortenerSerializer


class ShortenerViewSet(viewsets.ModelViewSet):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
