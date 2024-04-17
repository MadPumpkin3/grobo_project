from django.urls import reverse_lazy
from django.contrib.auth import login, logout
# redirect는 HTTP 리다이렉션을 수행하는 클래스로 사용자를 다른 url로 리다이렉트 할 수 있다.
# 확장성이 좋은 HttpResponseRedirect 클래스도 같은 기능을 함.
from django.shortcuts import redirect
from django.views import generic
from .models import User
from myapps.ai_data.models import Count
from myapps.form.users.user_form import LoginForm, JoinForm

# Create your views here.

# 사용자 로그인 뷰
class Login(generic.FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    
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
    
# 사용자 로그아웃 뷰
class Logout(generic.View):
    def post(self, request):
        logout(request)
        return redirect('users:login')

# 사용자 회원가입 뷰
class Join(generic.FormView):
    form_class = JoinForm
    template_name = 'users/join.html'
    success_url = reverse_lazy('users:login') # reverse_lazy(): URL을 역으로 해석하는 함수(즉, URL 패턴 이름을 사용하여 해당 URL를 생성하는데 사용)
    
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
    
    def form_valid(self, form):
        # 유효성을 통과한 폼 데이터를 받기 위해서는 form.cleaned_data로 불러와야 한다.
        cleaned_data = form.cleaned_data
        # create_user은 유저 데이터를 생성하는 메서드, 비밀번호를 해시로 저장해준다.
        user = User.objects.create_user(
            username = cleaned_data['username'],
            user_id = cleaned_data['user_id'],
            password = cleaned_data['password1'],
            email = cleaned_data['email'],
            profile_image = cleaned_data['profile_image'],
            short_description = cleaned_data['short_description'],
            default_main_page = cleaned_data['default_main_page'],
        )
        
        Count.objects.create(user=user)
        
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        return super().form_invalid(form)