from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve, reverse_lazy
from django.views import generic, View
from django.core.cache import cache

from .models import Post, PostComment, PreviewPost, PreviewImage
from myapps.form.posts.post_form import PostCustomEditorForm, PostCommentForm

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

# 포스트 생성 페이지를 보여주는 뷰
class MarkdownEditorView(generic.FormView):
    form_class = PostCustomEditorForm
    template_name = 'posts/posts_add.html'

# 실시간 미리보기 기능 구현 뷰(템플릿에서 온 Ajax 요청을 처리하는 뷰)
class PostPreview(View):
    http_method_names = ['post'] # 뷰가 POST 요청만 받게 설정
    
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
    http_method_names = ['post'] # 뷰가 POST 요청만 받게 설정
    
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': # 스크립트에서 .ajax로 데이터를 뷰로 보내면, 해당 요청 헤드에는 HTTP가 'XMLHttpRequest'로 들어감
            user = request.user # 요청을 보낸 요청자의 user 데이터 가져오기
            markdown_text = request.POST.get('content','')
            images_data = request.FILES.getlist('post_images_upload_field')
            
            # 사용자가 이미지 업로드가 처음인 경우
            if not PreviewPost.objects.filter(user=user).exists(): # .exists()함수는 테이블에 해당 레코드의 존재 여부를 bool 형식으로 반환
                first_post = True # 첫 이미지 업로드 시, 임시post 레코드 생성을 위해 'True'로 설정
                first_upload = True # 첫 이미지 업로드 시, 임시image 레코드 생성을 위해 'True'로 설정
                preview_post = self.preview_post_save(user, markdown_text, first_post) # markdown_text 데이터를 테이블에 저장하고 텍스트 형식으로 반환하는 메서드
                self.preview_image_save(preview_post, images_data, first_upload) # 키-값 쌍 배열의 이미지 파일을 테이블에 저장하고 파일 url 형식으로 반환하는 메서드
                preview_content = preview_post.content # 함수 실행 결과인 'preview_post'레코드 객체에서 'content'속성의 값만 호출하여 변수에 할당
                post_content = preview_post.content # 함수 실행 결과인 'preview_post'레코드 객체에서 'content'속성의 값만 호출하여 변수에 할당
                for image in PreviewImage.objects.filter(post=preview_post):
                    image_url = image.image_url.url # .url : 해당 이미지 객체를 호출인 가능한 형태의 url로 반환해주는 기능
                    preview_content += f'<br/> ![{image.id}번째 이미지]({image_url})' # 여러 이미지가 새로 방향으로 나열되기 위해 '<br/>'를 추가
                    post_content += f'\n<br/> ![{image.id}번째 이미지]({image_url})' # post_content 변수는 마크다운 필드에 들어갈 값으로 '문장'의 줄바꿈을 위해 '텍스트 필드'의 줄바꿈 키워드인 '/n'을 추가
            
            # 사용자가 이미지 업로드가 두 번 이상인 경우
            else:
                first_post = False # 두 번째 또는 그 이상 이미지 업로드 시, 기존 임시post 레코드를 가져오기 위해 'False'로 설정
                first_upload = False # 두 번째 또는 그 이상 이미지 업로드 시, 기존 임시image 레코드를 가져오기 위해 'False'로 설정
                preview_post = self.preview_post_save(user, markdown_text, first_post)
                preview_image_id = self.preview_image_save(preview_post, images_data, first_upload)
                preview_content = preview_post.content
                post_content = preview_post.content

                for id in preview_image_id:
                    image_objects = PreviewImage.objects.get(id=id)
                    image_url = image_objects.image_url.url
                    preview_content += f'<br/> ![{id}번째 이미지]({image_url})'
                    post_content += f'\n<br/> ![{id}번째 이미지]({image_url})'
            
            markdown_html = markdownify(preview_content)     
            return JsonResponse({'markdown_text': post_content, 'html_preview': markdown_html,})
            
        return JsonResponse({'error': "이미지 첨부 상식의 요청이 XML 방식의 요청이 아닙니다."}, status=400)
    
    def preview_post_save(self, user, markdown_text, first_post):
        
        if first_post == True: # 신규 작성인 경우, 임시 테이블에 신규 임시post 레코드 생성
            preview_post = PreviewPost.objects.create(user=user, content = markdown_text)
        else: # 추가 작성인 경우, 기존에 있던 임시 post 레코드 호출 및 내용(content 속성) 업데이트
            preview_post = PreviewPost.objects.filter(user=user).first()
            if preview_post:
                preview_post.content = markdown_text
                preview_post.save()
            
        return preview_post # 저장된 markdown_text를 텍스트 데이터 형식으로 반환
        
    def preview_image_save(self, preview_post, images_data, first_upload):
        
        if first_upload == True:
            for image in images_data:
                PreviewImage.objects.create(post = preview_post, image_url = image)
            
        else:
            preview_image_id = [] # 새로 추가될 이미지 id 저장을 위한 리스트 변수 선언
            for image in images_data:
                preview_image = PreviewImage.objects.create(post = preview_post, image_url = image)
                preview_image_id.append(preview_image.id) # 기존에 있던 이미지 id의 중복 추가를 방지하기 위해 새로 추가하는 이미지 id만 추출
            return preview_image_id

class PostSave(generic.FormView):
    http_method_names = ['post'] # 뷰가 POST 요청만 받게 설정
    success_url = reverse_lazy('posts:posts_add')
    
    def post(self, request, *args, **kwargs):
        form = PostCustomEditorForm(request.POST)
        image_data = request.FILES.getlist('post_images_upload_field')
        
        if image_data:
            if image_data.is_valid():
                return self.form_valid(form)
            
            else: 
                return self.form_invalid(form)
    
    def form_valid(self, form):
        # 이미지 데이터가 None인 경우, 저장 안함.
        return super().form_valid(form)
    
    def form_invalid(self, form):
        
        return super().form_invalid(form)