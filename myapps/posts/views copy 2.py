from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve, reverse_lazy, reverse
from django.views import generic, View

from .models import Post, PostImage, PostComment, PreviewPost, SearchKeyword
from .naver_api import NaverSearchAPI, text_transform, TextKeywordReader, Keyword_save
from myapps.users.models import UserSearchKeyword
from myapps.feeds.models import HashTag
from myapps.posts.models import Post
from myapps.common.views import user_authenticated
from myapps.form.posts.post_form import PostCustomEditorForm, PostCommentForm
from myapps.form.custom_form import validate_image

from markdownx.utils import markdownify

import time
import asyncio

# Create your views here.

# 포털 사이트 메인 페이지를 로드하는 뷰(검색 키워드 상위 3개와 관련된 데이터륿 보여주는 알고리즘 포함)
class PortalMainAPI(View):
    template_name = 'posts/portal_main.html'
    
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data()
        
        return JsonResponse(context)
    
    async def get_context_data(self):
        # 부모 클래스인 'TemplateView'에 내장되어 있고 템플릿에 데이터를 담당하는 'get_context_data()'메서드를 호출하여 데이터를 추가
        context = {}
        
        # 네이버 API도 비동기도 만들까? url 호출 중에 다른 작업 가능하게?
        algorithms_api_format = NaverSearchAPI()
        algorithms_data_list = await algorithms_api_format.algorithms_api_request(self.request.user)
        context['news_data_list'] = algorithms_data_list['news']
        context['shop_data_list'] = algorithms_data_list['shop']
        context['blog_data_list'] = algorithms_data_list['blog']
        
        login_button_text, login_button_url, login_yn = user_authenticated(self.request.user)
        
        # 사용자 맞춤 포스트 호출을 위한 비동기 작업 실행을 위해 'asyncio.run'으로 해당 기능 클래스 및 메서드 실행
        keyword_match_post_format = GetPostMatchKeyword()
        # 키워드 맞춤 포스트 탐색을 위해 비동기 방식으로 메서드 호출
        post_list, result_text, result_bool = await keyword_match_post_format.메인메서드(self.request.user)
        context['post_list'] = post_list
        context['result_text'] = result_text
            
        context['login_button_text'] = login_button_text
        context['login_button_url'] = login_button_url
        context['text'] = "환영합니다. 포털 메인 페이지입니다."
        return context

# 포털 검색 결과 페이지
class PortalSearchResults(generic.TemplateView):
    template_name = 'posts/portal_search_results.html'
    
    # 검색어 처리 진행
    def get_context_data(self, **kwargs):
        # 부모 클래스인 'TemplateView'에 내장되어 있고 템플릿에 데이터를 담당하는 'get_context_data()'메서드를 호출하여 데이터를 추가
        context = super().get_context_data(**kwargs)
        
        text = self.request.GET.get('portal_search_text', '') # 검색 창에 입력된 텍스트 데이터를 가져와서 할당
        
        text_reader_format = TextKeywordReader(text) # TextKeywordReader 클래스의 포맷 인스턴스 생성
        keyword_list = text_reader_format.text_keyword_reader() # 텍스트에서 키워드를 추출하는 전처리 메서드 실행하고, 결과를 keyword_list를 변수에 할당
        
        keyword_save_format = Keyword_save(self.request.user, keyword_list) # Keyword_save 클래스의 포맷 인스턴스 생성
        keyword_save_format.keyword_save() # keyword를 저장하는 메서드 실행
        
        # transformed_text = text_transform(text) # API url용 문자열로 변환(공백을 '+'로 변환)
        
        search_api_format = NaverSearchAPI()
        search_results = search_api_format.search_api_request(text)
        
        # news_results = data_thumbnail_extraction(search_results['news']) # 뉴스 데이터만 추출
        # webkr_results = data_thumbnail_extraction(search_results['webkr']) # 웹문서 데이터만 추출
        
        context['news_data_list'] = search_results['news']
        context['webkr_data_list'] = search_results['webkr']
        context['encyc_data_list'] = search_results['encyc']
        
        # 직접 만든 '유저 로그인 여부에 따라 버튼명과 연결 주소 그리고 로그인 여부'를 반환하는 함수
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
        if not request.user.is_authenticated:
            return redirect('users:login') # 로그인 상태가 아니면, 로그인 페이지로 이동
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
        
# 전체 API 응답 데이터 중 썸네일 데이터가 없을 경우, 썸네일용 이미지 추출 함수
def data_thumbnail_extraction(search_results):
    pass

# 키워드를 통해 post를 가져오는 클래스
class GetPostMatchKeyword():
    
    # 기본값으로 초기화
    def __init__(self):
        self.키워드리스트 = []
        self.키워드캐싱리스트 = [] # db내 키워드 인덱스가 변함에 따라 중복 키워드 확인을 방지하기 위해 50개의 키워드만 캐싱
        self.키워드리스트출처 = '' # 지정 단어 : Total, User, Mix
        self.키워드반복횟수 = 10
        self.키워드사용갯수 = 10
        self.키워드호출갯수 = 50
        self.키워드10개이상있음 = True
        
        self.재사용키워드리스트 = []
        
        self.반환포스트리스트 = []
        self.반환포스트갯수 = 3
        self.포스트호출id = 1 # 해당 키워드를 가진 포스트 중 [1]번째 포스트 가져오기
        self.실행완료여부 = False
        self.반환텍스트 = ''
    
    # 전체키워드 호출 코드의 재사용성을 위해 메서드로 제작
    def 전체키워드호출및저장_메서드(self):
        db_레코드_갯수 = SearchKeyword.objects.filter().count() # 메모리 절약을 위해 count로 레코드 갯수만 확인
        if db_레코드_갯수 > self.키워드호출갯수:
            self.키워드캐싱리스트 = list(SearchKeyword.objects.filter()[:self.키워드호출갯수])
        else:
            self.키워드캐싱리스트 = list(SearchKeyword.objects.filter())
    
    def 키워드리스트_선행_작업_메서드(self):
        # 키워드 반복 횟수 지정
        if len(self.키워드캐싱리스트) < self.키워드반복횟수: # 원본키워드 갯수가 키워드 초기 갯수(10개)보다 적을 경우
            self.키워드리스트 = self.키워드캐싱리스트
            self.키워드반복횟수 = len(self.키워드캐싱리스트) # 키워드 초기 갯수를 원본 키워드 초기 갯수(9이하)로 설정
            # self.키워드호출갯수 = len(self.키워드리스트) # 키워드 초기 호출 갯수를 원본 키워드 초기 갯수(9이하)로 설정
            self.키워드10개이상있음 = False
            self.키워드캐싱리스트.clear() # 요소를 삭제함으로써 메모리 확보하기 위해 캐싱 리스트 초기화
        else: # 키워드 갯수가 10개 이상인 경우
            self.키워드리스트 = self.키워드캐싱리스트[:self.키워드반복횟수] # 키워드 반복 횟수만큼만 호출
    
    # 키워드 맞춤 포스트 탐색 함수
    async def 키워드_맞춤_포스트_탐색_함수(self):
        # 키워드 맞춤 포스트 조사 실행
        for 키워드선택번호 in range(self.키워드반복횟수): # 키워드 리스트의 초기 갯수대로 반복
            키워드 = self.키워드리스트[키워드선택번호]
            포스트 = Post.objects.filter(tag = 키워드)[self.포스트호출id]
            if 포스트:
                self.반환포스트리스트.append(포스트)
                if self.포스트호출id > 1:
                    self.재사용키워드리스트.append(키워드)
            
            # 목표 포스트 수량 확인 후, 달성하면 위 while문 정지를 위해 True로 변환 뒤 반복 중단
            if len(self.반환포스트리스트) == self.반환포스트갯수:
                self.반환텍스트 = '맞춤형 포스트 추천'
                self.실행완료여부 = True
                break
            
        if len(self.반환포스트리스트) < self.반환포스트갯수:
            await self.세부_검증_메서드()
    
    # 실행 결과 검증 메서드
    async def 세부_검증_메서드(self):
        
        # 재사용 키워드 리스트에 키워드 존재 시, 설정 변경하여 재실행
        if self.재사용키워드리스트:
            self.포스트호출id += 1 # 해당 키워드의 다음번째 포스트 호출
            self.키워드리스트 = self.재사용키워드리스트 # 재사용키워드로 대체
            self.키워드반복횟수 = len(self.재사용키워드리스트)
            self.재사용키워드리스트 = [] # 재사용키워드리스트 초기화
            await self.키워드_맞춤_포스트_탐색_함수()
        
        elif self.키워드10개이상있음:
            self.포스트호출id = 0
            del self.키워드캐싱리스트[:self.키워드반복횟수]
            self.키워드리스트_선행_작업_메서드()
            await self.키워드_맞춤_포스트_탐색_함수()
            
        else: # 재사용 가능한 키워드도 없고, 추가 호출 가능한 키워드도 없을 경우         
            if self.키워드리스트출처 == 'User':
                if self.반환포스트리스트:
                    self.키워드리스트출처 = 'Mix'
                else:
                    self.키워드리스트출처 = 'Total'
                
                self.포스트호출id = 0
                self.전체키워드호출및저장_메서드()
                self.키워드리스트_선행_작업_메서드()
                await self.키워드_맞춤_포스트_탐색_함수()
                
            else:
                if self.반환포스트리스트:
                    self.반환텍스트 = '일부 포스트만 추천'
                else:
                    self.반환텍스트 = '추천 키워드 및 포스트 없음'
                    
                self.실행완료여부 = True
    
    def 반환데이터정리(self):
        최종반환데이터 = {
            '포스트출처': self.키워드리스트출처,
            '반환텍스트': self.반환텍스트,
            '반환포스트': self.반환포스트리스트,
        }
        return 최종반환데이터
    
    # 키워드 리스트 설정
    async def 메인메서드(self, user):
        
        # 유저 로그린 여부 따른 메서드 실행
        if user.is_authenticated and UserSearchKeyword.objects.filter(user=user).exists(): # 사용자가 로그인 상태이고, 해당 유저 키워드가 있으면 실행
            self.키워드리스트출처 = 'User'
            db_레코드_갯수 = UserSearchKeyword.objects.filter(user=user).count() # 메모리 절약을 위해 count로 레코드 갯수만 확인
            if db_레코드_갯수 > self.키워드호출갯수:
                self.키워드캐싱리스트 = list(UserSearchKeyword.objects.filter(user=user)[:self.키워드호출갯수])
            else:
                self.키워드캐싱리스트 = list(UserSearchKeyword.objects.filter(user=user))
            
        elif SearchKeyword.objects.filter().exists(): # 사용자가 비로그인 상태이면, 전체 키워드가 있으면 실행
            self.키워드리스트출처 = 'Total'
            self.전체키워드호출및저장_메서드()
            
        else: # 로그인 유저도 아니고, 전체 키워드에도 키워드가 없으면 실행
            self.반환텍스트 = '추천 키워드 없음.'
            최종반환데이터 = self.반환데이터정리() # 추후 출력 함수에 해당 데이터 첨부하여 실행
            return 최종반환데이터

        self.키워드리스트_선행_작업_메서드()
        await self.키워드_맞춤_포스트_탐색_함수()
        
        while self.실행완료여부 == False:
            await asyncio.sleep(2) # 반복 메서드들의 작업 완료 여부를 2초마다 확인
            
        최종반환데이터 = self.반환데이터정리()
        
        return 최종반환데이터