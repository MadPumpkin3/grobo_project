from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve, reverse_lazy, reverse
from django.views import generic, View

from .models import Post, PostImage, PostComment, PreviewPost
from .naver_api import NaverSearchAPI, text_transform, TextKeywordReader, Keyword_save
from myapps.users.models import User
from myapps.feeds.models import HashTag
from myapps.common.views import user_authenticated
from myapps.form.posts.post_form import PostCustomEditorForm, PostCommentForm
from myapps.form.custom_form import validate_image

from markdownx.utils import markdownify

# Create your views here.

# 데이터베이스에 있는 포스트 불러오는 뷰
class PortalMainAPI(generic.TemplateView):
    template_name = 'posts/portal_main.html'
    
    def get_context_data(self, **kwargs):
        login_button_text, login_button_url, login_yn = user_authenticated(self.request.user)
        context = super().get_context_data(**kwargs)
        context['login_button_text'] = login_button_text
        context['login_button_url'] = login_button_url
        context['text'] = "환영합니다. 포털 메인 페이지입니다."
        return context

# 포털 검색 결과 페이지
class PortalSearchResults(generic.TemplateView):
    template_name = 'posts/portal_search_results.html'
    
    # 검색어 처리 진행
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        text = self.request.GET.get('portal_search_text', '')
        
        text_reader_format = TextKeywordReader(text) # TextKeywordReader 클래스의 포맷 인스턴스 생성
        keyword_list = text_reader_format.text_keyword_reader() # 텍스트에서 키워드를 추출하는 전처리 메서드 실행하고, 결과를 keyword_list를 변수에 할당
        
        keyword_save_format = Keyword_save(self.request.user, keyword_list) # Keyword_save 클래스의 포맷 인스턴스 생성
        keyword_save_format.keyword_save() # keyword를 저장하는 메서드 실행
        
        # transformed_text = text_transform(text) # API url용 문자열로 변환(공백을 '+'로 변환)
        
        search_api_format = NaverSearchAPI()
        search_results = search_api_format.search_api_request(text)
        
        news_results = data_extraction(search_results['news']) # 뉴스 데이터만 추출
        encyc_results = data_extraction(search_results['encyc']) # 백과사전 데이터만 추출
        webkr_results = data_extraction(search_results['webkr']) # 웹문서 데이터만 추출
        
        context['news_data_list'] = search_results['news']
        context['encyc_data_list'] = search_results['encyc']
        context['webkr_data_list'] = search_results['webkr']
        
        login_button_text, login_button_url, login_yn = user_authenticated(self.request.user)
        context['login_button_text'] = login_button_text # nav태그에 들어가는 요소(로그인 여부에 따른 동적 버튼)
        context['login_button_url'] = login_button_url # nav태그에 들어가는 요소(로그인 여부에 따른 동적 버튼)
        context['text'] = '환영합니다. 포털 검색 결과 페이지입니다.'
        
        return context

# 포스트 디테일 페이지 보여주는 뷰
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/posts_detail.html'
    context_object_name = 'object'

# 포스트 생성 페이지를 보여주는 뷰
class MarkdownEditorView(generic.FormView):
    form_class = PostCustomEditorForm
    template_name = 'posts/posts_add.html'
    
    # 사용자 로그인 여부에 따른 동적으로 페이지 로드
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            default_main_page = user.default_main_page
            if default_main_page == 0:
                return redirect('posts:posts_main')
            else:
                return redirect('feeds:feeds_main')
        else:
            # super()로 부모 클래스'FormView'의 get메서드를 재호출해서 자식 클래스(내가 정의한 클래스: form_class, template_name를 적용한다.)
            return super().get(request, *args, **kwargs)

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
                preview_content = preview_post.content # 함수 실행 결과인 'preview_post'레코드 객체에서 'content'속성의 값만 호출하여 변수에 할당
                post_content = preview_post.content # 함수 실행 결과인 'preview_post'레코드 객체에서 'content'속성의 값만 호출하여 변수에 할당
                
                # 이미지를 저장하는 과정에서 유효성 검사도 같이 진행한다.
                is_valid, error_message = self.preview_image_save(preview_post, images_data, first_upload) # 키-값 쌍 배열의 이미지 파일을 테이블에 저장하고 파일 url 형식으로 반환하는 메서드

                # 이미지 파일의 유효성 검사가 False인 경우, 유효성 검사 함수에서 반환된 오류 메세지를 넣어서 반환
                if is_valid == False:
                    return JsonResponse({'error': error_message}, status=400)
                
                for image in PostImage.objects.filter(preview_post=preview_post):
                    image_url = image.image_url.url # .url : 해당 이미지 객체를 호출인 가능한 형태의 url로 반환해주는 기능
                    preview_content += f'<br/> ![{image.id}번째 이미지]({image_url})' # 여러 이미지가 새로 방향으로 나열되기 위해 '<br/>'를 추가
                    post_content += f'\n<br/> ![{image.id}번째 이미지]({image_url})' # post_content 변수는 마크다운 필드에 들어갈 값으로 '문장'의 줄바꿈을 위해 '텍스트 필드'의 줄바꿈 키워드인 '/n'을 추가
            
            # 사용자가 이미지 업로드가 두 번 이상인 경우
            else:
                first_post = False # 두 번째 또는 그 이상 이미지 업로드 시, 기존 임시post 레코드를 가져오기 위해 'False'로 설정
                first_upload = False # 두 번째 또는 그 이상 이미지 업로드 시, 기존 임시image 레코드를 가져오기 위해 'False'로 설정
                preview_post = self.preview_post_save(user, markdown_text, first_post)
                preview_content = preview_post.content
                post_content = preview_post.content
                
                is_valid, preview_image_id = self.preview_image_save(preview_post, images_data, first_upload)
                
                if is_valid == False:
                    return JsonResponse({'error': preview_image_id}, status=400)

                for id in preview_image_id:
                    image_objects = PostImage.objects.get(id=id)
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
                is_valid, error_message = validate_image(image)
                if is_valid:
                    PostImage.objects.create(preview_post = preview_post, image_url = image)
                else:
                    return False, error_message
                
            return True, None
            
        else:
            preview_image_id = [] # 새로 추가될 이미지 id 저장을 위한 리스트 변수 선언
            for image in images_data:
                is_valid, error_message = validate_image(image)
                if is_valid:
                    preview_image = PostImage.objects.create(preview_post = preview_post, image_url = image)
                    preview_image_id.append(preview_image.id) # 기존에 있던 이미지 id의 중복 추가를 방지하기 위해 새로 추가하는 이미지 id만 추출
                else:
                    return False, error_message
                
            return True, preview_image_id

# 포스트를 최종적으로 저장하는 뷰
class PostSave(generic.FormView):
    http_method_names = ['post'] # 뷰가 POST 요청만 받게 설정
    form_class = PostCustomEditorForm # 폼 초기화
    
    def form_valid(self, form):
        user = self.request.user
        
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        tags = form.cleaned_data['tag']
        
        post = Post.objects.create(user = user, title = title, content = content)
        
        for tag_name in tags:
            tag, created = HashTag.objects.get_or_create(tag_name = tag_name) # get_or_create: 지정된 객체가 있으면 가져오고 없으면 새로 생성하는 함수
            post.tag.add(tag) # 테이블의 'ManyToManyField'인 경우에만 사용 가능함 함수, 해당 'ManyToManyField'에 객체를 '추가'하는 기능
        
        if PreviewPost.objects.filter(user=user).exists():
            preview_post = PreviewPost.objects.filter(user=user).first()
            if PostImage.objects.filter(preview_post=preview_post).exists():
                preview_images = PostImage.objects.filter(preview_post=preview_post) # 이미지 객체들을 쿼리셋 형식으로 가져옴(.all()을 쓰면 리스트 형식으로 가져옴)
                for image in preview_images: # 쿼리셋 형식의 이미지 객체들을 하나씩 꺼내옴.
                    image.post = post
                    image.save()
                    
            # 사용자의 preview_post가 있을 때, preview_post 삭제 함수 실행(preview_post 객체가 삭제되면, PostImage에 연결된 preview_post필드의 값은 자동으로 None 처리됨.)
            preview_post_delete(user) 
        
        url = reverse('posts:posts_detail', kwargs={'pk': post.id})
        
        return redirect(url)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
# 미리보기 포스트 데이터를 삭제하는 함수
def preview_post_delete(user):
    if PreviewPost.objects.filter(user=user).exists():
        preview_post = PreviewPost.objects.filter(user=user).first()
        preview_post.delete()
        
# 전체 API 응답 데이터에서 특정 '키워드'에 맞는 데이터만 추출
def data_extraction(search_results):
    pass