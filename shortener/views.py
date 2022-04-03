from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Shortener
from .permissions import IsOwnerOrReadOnly
from .serializers import ShortenerSerializer


class ShortenerViewSet(viewsets.ModelViewSet):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def redirect_url(request, short_id):
    shortener = get_object_or_404(Shortener, short_id=short_id)
    return HttpResponseRedirect(shortener.link)
