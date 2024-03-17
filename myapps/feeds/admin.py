from django.contrib import admin
from .models import Feed, FeedComment, FeedImage, HashTag
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
import admin_thumbnails


# Register your models here.

class FeedCommentInline(admin.TabularInline):
    model = FeedComment
    extra = 1
    
@admin_thumbnails.thumbnail('image_url')
class FeedImageInline(admin.TabularInline):
    model = FeedImage
    extra = 1
    

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    list_filter = ('user', 'created', 'tag')
    search_fields = ('user', 'created', 'tag')
    fieldsets = [
        (None, {'fields': ('user',)}),
        ('주요내용', {'fields': ('context', 'tag')}),
    ]
    
    inlines = [FeedImageInline, FeedCommentInline]
    
    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    
@admin.register(FeedComment)
class FeedCommnetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feed', 'created')
    fieldsets = [
        (None, {'fields': ('user',)}),
        ('주요내용', {'fields': ('comment',)}),
    ]
    
@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name')