from django.urls import reverse_lazy
from django.contrib.auth import login, logout
# redirect는 HTTP 리다이렉션을 수행하는 클래스로 사용자를 다른 url로 리다이렉트 할 수 있다.
# 확장성이 좋은 HttpResponseRedirect 클래스도 같은 기능을 함.
from django.shortcuts import redirect
from django.views import generic
from .models import User
from myapps.form.users.user_form import LoginForm, JoinForm

# Create your views here.

class Login(generic.FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    # success_url : 제출 후 이동할 url 지정(폼이 통과될 경우 결과 같으로 전송)
    # success_url = reverse_lazy('posts:posts_main')
    
    # 폼 유효성 통과 시 실행되는 메서드
    def form_valid(self, form):
        user = form.cleaned_data['user']
        default_main_page = form.cleaned_data['default_main_page']
        login(self.request, user)
        
        if default_main_page == 0:
            return redirect('posts:posts_main')
        else:
            return redirect('feeds:feeds_main')
        
    # 폼 유효성 검사 실패 시 실행되는 메서드
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class Logout(generic.View):
    def post(self, request):
        logout(request)
        return redirect('users:login')
    
class Join(generic.FormView):
    form_class = JoinForm
    template_name = 'users/join.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        pass
    
    def form_invalid(self, form):
        return super().form_invalid(form)
        
    