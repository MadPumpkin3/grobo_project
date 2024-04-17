from django.shortcuts import redirect, render
from django.views import View
from django.urls import resolve, reverse
from urllib.parse import urlparse
from django.contrib.auth import authenticate

# Create your views here.

class PageSwitching(View):
    def post(self, request):
        # 템플릿에서 받은 current_url = 전체 주소(예: http://example.com/posts/posts_main/)
        current_url = request.POST.get('current_url', '')
        # 전체 주소를 urlparse() 함수를 사용하여, 전체 주소를 구분하여 받을 수 있도록 선 작업
        parsed_url = urlparse(current_url)
        # urlparse()함수 기능인 경로 부분만을 추출하는 path로 URL 경로만 추출 (예: '/posts/posts_main/')
        # 아래 resolve()함수를 통해 URL패턴과 비교하려면 URL 경로 맨 앞에 '/' 포함된 URL 경로가 필요 (조건문으로 '/'가 없을 경우 포함되도록 작업 )
        path = parsed_url.path if parsed_url.path.startswith('/') else '/' + parsed_url.path
        # resolve 속성 중 하나인 'namespace'로, 입력된 URL경로를 가지고 있는 app_name을 반환하는 속성이다.
        app_name = resolve(path).namespace
        
        # 가져온 app_name에 따라 redirect 값을 지정
        if app_name == 'posts':
            return redirect('feeds:feeds_main')
        elif app_name == 'feeds':
            return redirect('posts:posts_main')
        else:
            # 중립 페이지의 경우, 유저의 기본 메인 페이지로 이동
            user_main_page = request.user.default_main_page # 유저의 기본 메인 페이지 값 가져오기
            if user_main_page == 0:
                return redirect('posts:posts_main')
            else:
                return redirect('feeds:feeds_main')
            
# 유저 로그인 여부에 따른 버튼 변환
def user_authenticated(user):
    if user.is_authenticated:
        return "Logout", reverse('users:logout'), True
    else:
        return "Login", reverse('users:login'), False     