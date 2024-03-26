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
from .views import Index, LoginStatus
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    # 웰컴 페이지(index)에 로그인 버튼 클릭시 login_statue 실행 후, 결과에 따라 페이지 이동
    path('login_status/', LoginStatus.as_view(), name='login_status'),
    # 모델, 폼, 템플릿에서 markdown을 사용하기 위해 설정
    path('markdownx/', include('markdownx.urls')),
    path('users/', include('myapps.users.users_urls')),
    path('posts/', include('myapps.posts.posts_urls')),
    path('feeds/', include('myapps.feeds.feeds_urls')),
    path('ai_data/', include('myapps.ai_data.ai_data_urls')),
    path('common/', include('myapps.common.common_urls')),
]

# 저장된 이미지를 불러오기 위한 설정
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT,
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]