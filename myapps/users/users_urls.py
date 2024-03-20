from django.urls import path, include
from .views import Login, Logout, Join, LoginStatus

app_name = 'users'

urlpatterns = [
    path('loginstatus/', LoginStatus.as_view(), name='login_status'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('join/', Join.as_view(), name='join'),
]