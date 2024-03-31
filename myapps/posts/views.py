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
        return JsonResponse({'error':"실시간 미리보기 기능의 요청이 XML 방식의 요청이 아닙니다."}, status=400)
    
# 포스트 생성 페이지에 이미지를 첨부시 반환하는 뷰
class PostImageUpload(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': # 스크립트에서 .ajax로 데이터를 뷰로 보내면, 해당 요청 헤드에는 HTTP가 'XMLHttpRequest'로 들어감
            user = request.user # 요청을 보낸 요청자의 user 데이터 가져오기
            markdown_text = request.POST.get('content','')
            images_data = request.FILES.getlist('post_images_upload_field')
            if not PreviewPost.objects.filter(user=user).exists():
                preview_post = self.preview_post_save(user, markdown_text) # markdown_text 데이터를 테이블에 저장하고 텍스트 형식으로 반환하는 메서드
                preview_image = self.preview_image_save(preview_post, images_data) # 키-값 쌍 배열의 이미지 파일을 테이블에 저장하고 파일 url 형식으로 반환하는 메서드
                post_conent = preview_post.content
                for image in preview_image:
                    post_conent += f'<br/> ![{image.id}번째 이미지]({image.image_url})'
                markdown_html = markdownify(post_conent)
                
                print(type(post_conent), post_conent)
                print()
                print(type(markdown_html), markdown_html)
                print()
                return JsonResponse({'markdown_text': post_conent, 'markdown_html': markdown_html,})
                
            return JsonResponse({'error': "기존 데이터가 존재합니다."}, status='400')
            
        return JsonResponse({'error': "이미지 첨부 상식의 요청이 XML 방식의 요청이 아닙니다."}, status='400')
    
    def preview_post_save(self, user, markdown_text):
        preview_post = PreviewPost.objects.create(user=user, content = markdown_text)
        return preview_post # 저장된 markdown_text를 텍스트 데이터 형식으로 반환
        
    def preview_image_save(self, preview_post, images_data):
        preview_image = []
        for image in images_data:
            preview_image_save = PreviewImage.objects.create(post = preview_post, image_url = image)
            preview_image.append(preview_image_save)
        
        return preview_image
        
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