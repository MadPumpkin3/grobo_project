from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSearchKeyword
from django.db import models
from django.forms import RadioSelect, CheckboxSelectMultiple
from myapps.common.models import DefaultMainPageChoices
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model

# Register your models here.

# user 추가 시, 모든 속성을 일괄로 입력하고 싶어서 user 추가 폼을 변경하는 클래스(그러나 제대로 안돼서 포기..)
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User

class FollowingInline(admin.TabularInline):
    model = User.following.through
    fk_name = "follow_to"
    verbose_name = '내가 팔로우한 사람'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1
    
class FollowersInline(admin.TabularInline):
    model = User.following.through
    fk_name = "follow_from"
    verbose_name = '나를 팔로우한 사람'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'user_id', 'username', 'email', 'is_staff', 'login_at', 'updated_at', 'created_at')
    # 관리자가 아래 필드를 기준으로 사용자를 필터링 할 수 있다.
    list_filter = ('username', 'created_at', 'login_at')
    # 관리자가 아래 필드를 기준으로 사용자를 검색할 수 있다.
    search_fields = ('user_id', 'username', 'email')
    fieldsets = [
        (None, {'fields': ('user_id', 'password')}),
        ('개인정보', {'fields': ('username', 'email')}),
        ('추가필드', {'fields': ('profile_image', 
                             'short_description', 
                             'default_main_page')}),
        ('좋아요', {'fields': ('like_posts', 'like_feeds')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    ]
    
    # 관리자 페이지에서 라디오 버튼으로 기본 메인 페이지 설정 가능하도록 설정
    # IntegerField는 위 fieldset에 필드 중 IntegerField 대상으로 설정한다는 뜻
    # RadioSelect는 라디오 버튼으로 구현한다는 것
    # choices=DefaultMainPageChoices는 선택 사항을 DefaultMainPageChoices클래스에 정의된 방식대로 한다는 뜻
    formfield_overrides = {
        # models.ManyToManyField: {"widget": CheckboxSelectMultiple}, # 아래에 있는 'filter_horizontal' 속성과 공존할 수 없다.
        models.IntegerField: {'widget':RadioSelect(choices=DefaultMainPageChoices)}
    }
    
    # filter_horizontal은 User모델에 ManyToManyField로 작성된 필드를 관리자 페이지에 수평으로 나열한다.
    filter_horizontal=('like_posts', 'like_feeds') 
    
    inlines = [FollowingInline, FollowersInline]
    
    # 필드 정렬 기준('username'을 기준으로 오름차순으로 정렬)
    ordering = ['username']
    
    # user 추가 시, 모든 속성을 일괄로 입력하고 싶어서 user 추가 폼을 변경하는 클래스(그러나 제대로 안돼서 포기..)
    # add_form = CustomUserCreationForm
    
@admin.register(UserSearchKeyword)
class UserSearchKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_at')

    filter_horizontal=('search_keyword',)