from django.views import generic
from myapps.users.models import User
from django.shortcuts import redirect, render
from django.urls import resolve

class Index(generic.View):
    template_name = 'index.html' # 사용할 템플릿 파일 지정
    
    def get(self, request):
        return render(request, self.template_name)
    # model = User
    
    # def get_context_data(self, **kwargs): # **kwargs : Index 클래스에서 받은 request객체를 받는다.
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'Hellow, Grobo!'
    #     return context
    
# 초기 페이지(index)에서 사용자의 로그인 여부에 따라 '로그인' 클릭시 이동되게 설정
class LoginStatus(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            url = request.user.default_main_page
            if url == 0:
                return redirect('posts:posts_main')
            else:
                return redirect('feeds:feeds_main')
        else:
            return redirect('users:login')
        
class PageSwitching(generic.View):
    def post(self, request):
        # 유저의 기본 메인 페이지 값 가져오기
        user_main_page = request.user.default_main_page
        # 현재 페이지의 주소 가져오기
        app_name = resolve(request.path_info).app_names
        # 가져온 현재 페이지 주소가 속한 app_name 가져오기
        # app_name = current_url.app_names
        
        # 가져온 app_name에 따라 redirect 값을 지정
        if app_name == 'posts':
            return redirect('feeds:feeds_main')
        elif app_name == 'feeds':
            return redirect('posts:posts_main')
        else:
            # 중립 페이지의 경우, 유저의 기본 메인 페이지로 이동
            if user_main_page == 0:
                return redirect('posts:posts_main')
            else:
                return redirect('feeds:feeds_main')