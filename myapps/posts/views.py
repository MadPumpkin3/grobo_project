from django.http import HttpResponse
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
        form = PostCreateForm(request.POST, request.FILES)
        # form_data = request.POST
        # file_data = request.FILES
        
        context = {
            'form': form,
            'title': '통신 잘됨',
        }
        
        return render(request, self.template_name, context)
        