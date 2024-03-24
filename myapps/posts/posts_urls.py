from django.urls import path
from .views import PortalMainAPI, PostAdd, PostImageUpload

app_name = 'posts'

urlpatterns = [
    path('posts_main/', PortalMainAPI.as_view(), name='posts_main'),
    path('posts_add/', PostAdd.as_view(), name='posts_add'),
    path('posts_images_upload/', PostImageUpload.as_view(), name='posts_images_upload'),
]