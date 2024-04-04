from django.urls import path
from .views import PortalMainAPI, MarkdownEditorView, PostPreview, PostImageUpload, PostSave, PostDetailView

app_name = 'posts'

urlpatterns = [
    path('posts_main/', PortalMainAPI.as_view(), name='posts_main'),
    path('posts_add/', MarkdownEditorView.as_view(), name='posts_add'),
    path('posts_save/', PostSave.as_view(), name='posts_save'),
    path('posts_preview', PostPreview.as_view(), name='posts_preview'),
    path('posts_images_upload/', PostImageUpload.as_view(), name='posts_images_upload'),
    path('posts_detail/<int:post_id>/', PostDetailView.as_view(), name='posts_detail'),
]