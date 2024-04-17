from django.urls import path
from .views import PageSwitching

app_name = 'common'

urlpatterns = [
    path('page_switching/', PageSwitching.as_view(), name='page_switching'),
]