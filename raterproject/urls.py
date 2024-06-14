from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import UserViewSet
from django.conf import settings
from django.conf.urls.static import static
from raterapi.views import GameViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameViewSet, 'game')

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)