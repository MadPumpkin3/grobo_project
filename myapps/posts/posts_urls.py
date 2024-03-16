from django.urls import path
from .views import PortalMainAPI

app_name = 'posts'

urlpatterns = [
    path('main/', PortalMainAPI.as_view(), name='posts_main'),
]