from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve
from .models import Post, PostComment
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
    template_name = 'posts/posts_add.html'
    
    def post(self, request):
        # request.POST는 데이터가 딕셔너리 형태인 'field_name_1': 'value_1' 으로 저장되어 있다.
        form_data = request.POST
        # request.FILES는 이미지가 딕셔너리 형태인 'file_field_name_1': <UploadedFile object> 으로 저장되어 있다.
        file_data = request.FILES
        
        content_data = form_data.get('content')
        
        # 이미지 파일의 url을 지정할 리스트를 생성
        image_urls = []
        
        for image_name, image_file in file_data.items():
            cache.set(image_name, image_file, timeout=86400)
            image_url = cache.get(image_name)
            content_data += f'\n {image_url}'
            
        
        # for image in file_data:
        #     cache.set(image[0], image[1], timeout=86400)
        #     context_data = f'\r {image[1]}'
        
        context = {
            'title': form_data.get('title'),
            'content': content_data,
            'tag': form_data.get('tag'),
        }
        
        print(context)
        
        # JsonResponse() : 주어진 데이터를 JSON형식으로 직렬화하고, 이를 HTTP 응답으롤 반환한다.
        # 그러면 템플릿의 자바스크립트에서 JSON형식의 데이터를 받고, 이 데이터를 자바스크립트로 바꿔서 사용한다.
        return JsonResponse(context)
    
        # (중요!!) django와 자바스크립트 간의 데이터 통신에서 JSON형식을 사용하는 것이 일반적이다.
        # (중요!!) 자바스크립트 > django 데이터 전송 시 별다른 변환x
        # (중요!!) django > 자바스크립트 데이터 전송 시 JSON형식으로 변환 > 자바스크립트에서 JSON형식의 데이터를 자바스크립트 데이터로 변환
        
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