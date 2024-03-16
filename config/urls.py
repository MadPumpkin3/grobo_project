"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .view import Index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('users/', include('myapps.users.users_urls')),
    path('posts/', include('myapps.posts.posts_urls')),
    path('feeds/', include('myapps.feeds.feeds_urls')),
    path('ai_data/', include('myapps.ai_data.ai_data_urls')),
]

urlpatterns += static(
    prefix=settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT,
    )