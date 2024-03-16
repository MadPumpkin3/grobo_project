from django.urls import path
from .views import AiMain

app_name = 'ai_data'

urlpatterns = [
    path('main/', AiMain.as_view(), name='ai_data_main'),
]