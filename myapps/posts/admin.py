from django.contrib import admin
from .models import Post, PostComment, PostImage
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
import admin_thumbnails
from markdownx.admin import MarkdownxModelAdmin
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget

# Register your models here.

class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1
    verbose_name = "댓글"
    
@admin_thumbnails.thumbnail("image_url") # 관리자 페이지 - post생성 페이지에서 업로드한 사진을 보여주는 기능
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    verbose_name = "이미지 업로드"

# class PostAdmin(admin.ModelAdmin):

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ('id', 'user', 'title', 'created')
    list_filter = ('user', 'tag', 'created')
    search_fields = ('user', 'tag')
    fieldsets = [
        (None, {'fields': ('user',)}), # 기본적으로 레코드 생성 form에는 id 필드가 없다.(id는 자동 생성되기 때문에 지정할 필요가 없어서)
        ('주요내용', {'fields': ('title', 'context')}),
        ('추가내용', {'fields': ('tag',)}),
    ]
    
    inlines = [PostImageInline, PostCommentInline]
    
    # Post모델의 M2M필드인 'tag'필드가 기본 필드 형태로는 가시성과 조작성이 좋지 않아서 개선하기 위해 하는 작업
    # formfield_overrides : 특정 필드 유형에 대한 기본 입력 위젯을 재정의하는데 사용되는 옵션
    # 필드에 옵션을 적용하려면 필드(tag필드)와 연결된 모델(hashtag)을 관리자 페이지에 등록해야 한다.
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
        MarkdownxField: {"widget": AdminMarkdownxWidget},
    }
 
@admin.register(PostComment)    
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created')