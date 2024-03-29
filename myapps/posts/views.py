from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve
from .models import Post, PostComment, PreviewPost, PreviewImage
from django.views import generic, View
from myapps.form.posts.post_form import PostCustomEditorForm, PostCommentForm
from django.core.cache import cache
from markdownx.utils import markdownify

# Create your views here.

# 데이터베이스에 있는 포스트 불러오는 뷰
class PortalMainAPI(generic.ListView):
    template_name = 'posts/portal_main.html'
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'PortalMainAPI 테스트용'
        return context

# 포스트 생성 페이지에 마크다운 필드를 보여주는 뷰
class MarkdownEditorView(generic.FormView):
    form_class = PostCustomEditorForm
    template_name = 'posts/posts_add.html'
    
    # def get(self, request):
    #     return render(request, 'posts/posts_add.html')

# 포스트 생성 페이지 뷰
class PostPreview(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            title = request.POST.get('title', '')
            markdown_text = request.POST.get('markdown_text', '')
            tag = request.POST.get('tag', '')
            html_preview = markdownify(markdown_text)
            return JsonResponse({
                'title': title,
                'html_preview': html_preview,
                'tag': tag,
                })
        return JsonResponse({}, status=400)
    
# 포스트 생성 페이지에 이미지를 첨부시 반환하는 뷰
class PostImageUpload(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = request.user
            markdown_text = request.POST.get('markdown_text', '')
            images_data = request.POST.get('image_data')
            if not PreviewPost.objects.filter(user=user).exists():
                preview_post = self.preview_post_save(user, markdown_text)
                preview_image = self.preview_image_save(preview_post, images_data)
            return JsonResponse({}, status=400)
            
        return JsonResponse({}, status=400)
    
    def preview_post_save(self, user, markdown_text):
        preview_post = PreviewPost.objects.create(user=user, content = markdown_text)
        return(preview_post)
        
    def preview_image_save(self, preview_post, images_data):
        # .items()함수: 딕셔너리 형시의 데이터를 키와 값으로 나누어 처리할 수 있게 해준다.
        for key, value in images_data.items():
            PreviewImage.objects.create(post = preview_post, image_url = value)
        
# 포스트를 저장하는 뷰
class PostSave():
    template_name = 'posts/posts_add.html'
    success_url = ''
    def form_valid(self, form):
        print('입력 성공')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print('오류 발생')
        return super().form_invalid(form)