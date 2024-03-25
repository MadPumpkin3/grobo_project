from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve
from .models import Post, PostComment
from django.views import generic
from myapps.form.posts.post_form import PostCreateForm, PostCommentForm

# Create your views here.

class PortalMainAPI(generic.ListView):
    template_name = 'posts/portal_main.html'
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'PortalMainAPI 테스트용'
        return context

# 포스트를 저장하는 클래스
class PostAdd(generic.FormView):
    form_class = PostCreateForm
    template_name = 'posts/posts_add.html'
    success_url = ''
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
# 포스트에 이미지를 넣고 반환하는 클래스
class PostImageUpload(generic.View):
    template_name = 'posts/posts_add.html'
    
    def post(self, request):
        form_data = request.POST
        file_data = request.FILES
        context = {
            'title': form_data.get('title'),
            'context': form_data.get('context'),
            'tag': form_data.get('tag'),
        }
        
        # JsonResponse() : 주어진 데이터를 JSON형식으로 직렬화하고, 이를 HTTP 응답으롤 반환한다.
        # 그러면 템플릿의 자바스크립트에서 JSON형식의 데이터를 받고, 이 데이터를 자바스크립트로 바꿔서 사용한다.
        return JsonResponse(context)
    
        # (중요!!) django와 자바스크립트 간의 데이터 통신에서 JSON형식을 사용하는 것이 일반적이다.
        # (중요!!) 자바스크립트 > django 데이터 전송 시 별다른 변환x
        # (중요!!) django > 자바스크립트 데이터 전송 시 JSON형식으로 변환 > 자바스크립트에서 JSON형식의 데이터를 자바스크립트 데이터로 변환
        