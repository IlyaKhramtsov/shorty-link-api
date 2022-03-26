from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shortener.views import ShortenerViewSet

router = routers.SimpleRouter()
router.register(r'shortener', ShortenerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
