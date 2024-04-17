from django.urls import path
from .views import Login, Logout, Join

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('join/', Join.as_view(), name='join'),
]