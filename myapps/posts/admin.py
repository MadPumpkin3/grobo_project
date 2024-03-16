from django.contrib import admin
from .models import Post, PostComment

# Register your models here.

class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created')
    list_filter = ('user', 'tag', 'created')
    search_fields = ('user', 'tag')
    fieldsets = [
        (None, {'fields': ('id', 'user')}),
        ('주요내용', {'fields': ('title', 'context')}),
        ('이미지', {'fields': ('image_url',)}),
        ('추가내용', {'fields': ('tag',)}),
        ('작성일시', {'fields': ('created',)}),
    ]
    
    inlines = [PostCommentInline]
 
@admin.register(PostComment)    
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created')