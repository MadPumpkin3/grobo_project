from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

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
    list_display = ('id', 'user_id', 'username', 'email', 'is_staff', 'login_at')
    # 관리자가 아래 필드를 기준으로 사용자를 필터링 할 수 있다.
    list_filter = ('username', 'created_at', 'login_at')
    # 관리자가 아래 필드를 기준으로 사용자를 검색할 수 있다.
    search_fields = ('user_id', 'username', 'email')
    fieldsets = [
        (None, {'fields': ('user_id', 'password')}),
        ('개인정보', {'fields': ('username', 'email')}),
        ('추가필드', {'fields': ('profile_image', 'short_description')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    ]
    
    # filter_horizontal은 User모델에 ManyToManyField로 작성된 필드를 관리자 페이지에 수평으로 나열한다.
    filter_horizontal=('like_posts', 'like_feeds') 
    
    inlines = [FollowingInline, FollowersInline]