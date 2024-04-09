from django.urls import path
from .views import Platform_main

app_name = 'feeds'

urlpatterns = [
    path('', Platform_main.as_view(), name='feeds_main'),
]