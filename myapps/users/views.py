from django.shortcuts import render
from django.views.generic import FormView
from .models import User
from myapps.form.users.user_form import LoginForm, JoinForm

# Create your views here.

class Login(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    # success_url : 제출 후 이동할 url 지정(폼이 통과될 경우 결과 같으로 전송)
    success_url = ''
    
    # 폼 유효성 통과 시 실행되는 메서드
    def form_valid(self, form):
        return super().form_valid(form)
        
    # 폼 유효성 검사 실패 시 실행되는 메서드
    def form_invalid(self, form):
        return super().form_invalid(form)