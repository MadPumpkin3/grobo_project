from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve, reverse_lazy, reverse
from django.views import generic, View

from .models import Post, PostImage, PostComment, PreviewPost
from .naver_api import NaverSearchAPI, text_transform, TextKeywordReader, Keyword_save
from myapps.users.models import UserSearchKeyword
from myapps.feeds.models import HashTag
from myapps.posts.models import Post
from myapps.common.views import user_authenticated
from myapps.form.posts.post_form import PostCustomEditorForm, PostCommentForm
from myapps.form.custom_form import validate_image

from markdownx.utils import markdownify

# Create your views here.

# 포털 사이트 메인 페이지를 로드하는 뷰(검색 키워드 상위 3개와 관련된 데이터륿 보여주는 알고리즘 포함)
class PortalMainAPI(generic.TemplateView):
    template_name = 'posts/portal_main.html'
    
    def get_context_data(self, **kwargs):
        # 부모 클래스인 'TemplateView'에 내장되어 있고 템플릿에 데이터를 담당하는 'get_context_data()'메서드를 호출하여 데이터를 추가
        context = super().get_context_data(**kwargs) 
        
        algorithms_api_format = NaverSearchAPI()
        algorithms_data_list = algorithms_api_format.algorithms_api_request(self.request.user)
        context['news_data_list'] = algorithms_data_list['news']
        context['shop_data_list'] = algorithms_data_list['shop']
        context['blog_data_list'] = algorithms_data_list['blog']
        
        login_button_text, login_button_url, login_yn = user_authenticated(self.request.user)
        
        keyword_match_post_format = GetPostMatchKeyword()
        if login_yn:
            post_list, result_text, result_bool = keyword_match_post_format.user_keyword_match_post(self.request.user)
        else:
            post_list, result_text, result_bool = keyword_match_post_format.total_keyword_match_post()
            
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
    
    def __init__(self):
        self.data_detaile = {}
        self.data_list = []
        self.result_text = ""
        self.result_bool = True
        
        self.keyword_number = 10 # 사용하려는 키워드 수 ** 중요: 키워드의 갯수는 포스트의 갯수를 넘을 수 없음.
        self.post_number = 3 # 호출하려는 총 포스트 수(키워드 1개당 1~2개 호출) 
        # 포스트보다 키워드 수가 부족한 경우, 부족한 만큼 키워드 인덱스(오름차순)에 있는 포스트를 1번 더 호출(인덱스 계산을 위해 -1을 포함)
        self.keyword_index = self.post_number - self.post_number - 1
        
    def user_keyword_match_post(self, user):
        user_keyword_list = []
        post_yn_bool = True
        
        keyword_focus_line = 10
        keyword_last_line = 20
        
        post_data_list = []
        post_get_number = 3
        
        post_true_keyword = [] # 포스트가 있던 키워드일 경우, 해당 키워드를 저장
        
        post_true_keyword_index = 0
        post_true_keyword_list = []
        post_true_keyword_number = 2
        
        user_keywords = UserSearchKeyword.objects.filter(user = user)
        
        if user_keywords.exists():
            user_keywords_number = len(user_keywords)
            
            if user_keywords_number < keyword_focus_line: # 해당 유저의 키워드가 '10'개 미만인 경우
                keyword_focus_line = user_keywords_number # 최소 1개 이상, 최대 9개 이하

            for focus_number in range(keyword_focus_line):
                index, keyword = enumerate(user_keywords[focus_number])
                tag_posts = Post.objects.filter(tag = keyword)
                if tag_posts.exists():
                    post = tag_posts[0]
                    self.data_detaile = {
                        'id': post.id,
                        'title': post.title,
                        'content': post.content,
                    }
                    post_data_list.append(self.data_detaile)
                    post_true_keyword.append({index : len(tag_posts)}) # 포스트 있을 경우, 해당 키워드의 인덱스를 키로 하고 키워드 맞춤 포스트의 갯수를 값으로 한다.
                
                # 정상 성공 여부 판단
                if len(post_data_list) == post_get_number: # 가져온 포스트 리스트 내 객체의 갯수와 찾으려는 포스트 갯수가 일치할 경우, 작업 성공으로 반복 중지
                    break # for문 중지
                
                # 유저 포커스 키워드 위치 및 여부
                elif index == keyword_focus_line - 1: # 지정된 갯수만큼 포스트를 가져오지 못했는데 초기 지정된 반복횟수가 끝난 경우
                    if len(post_data_list) == 0: # 데이터가 없는 상태(즉, 포스터가 있는 키워드가 없는 경우)
                        # 유저 키워드 갯수가 포커스 기준 선(갯수)보다 많고, 포커스 기준 선(갯수)가 최대 기준 선(갯수)보다 낮을 경우 (즉, 포커스가 50보다 낮거나 같은 경우)
                        if user_keywords_number >= keyword_focus_line and keyword_focus_line <= keyword_last_line: 
                            keyword_focus_line += 1 # 유저 키워드의 다음 인덱스를 읽기 위해 포커스 기준 선(갯수)를 1 높인다.
                        else:
                            self.data_list, self.result_text, self.result_bool = self.total_keyword_match_post()
                    
                    elif len(post_data_list) > 0:
                        keyword = post_true_keyword[]
                        for key, value in keyword:
                            if value >= 2:
                                keyword_focus_line
                                
                        
                    
            self.result_text = "사용자 맞춤 포스트입니다."
            self.result_bool = True
        
        else:
            self.data_list, self.result_text, self.result_bool = self.total_keyword_match_post()
            
        return self.data_list, self.result_text, self.result_bool
        

    def total_keyword_match_post(self):
        pass
    
    
    def get_post(self):
        pass
    
    

user_keywords_number = 3 # 사용하려는 키워드 갯수
user_keywords_line = 3 # 전체 키워드 갯수를 나누려는 수(키워드가 많을 경우 나눠서 상위 33%에 속하는 것만 진행)

# 하루 구글 총 검색 횟수 : 12억
# 지구 총 인구 : 77억
# 지구 총 인구 / 구글 총 검색 횟수 = 6.41
# 대략적으로 하루에 한 사람이 검색하는 횟수 = 7번
# 한 문장에 들어가는 단어의 평균 갯수 : 10~20개 (평균 15개)
# 7번 x 10개(최소) = 70개
# 한 사람이 검색할 때 사용하는 하루 단어의 갯수 = 70개
keyword_search_max_number = 70 # 알고리즘에 사용하려는 최대 키워드 갯수(유저 키워드가 이 수를 넘으면 > 전체 키워드 검색으로 넘어감.)
keyword_search_min_number = 10 # 알고리즘에 사용하려는 최소 키워드 갯수(유저 키워드가 이 수를 넘으면 다음 10개의 키워드로 지정)
