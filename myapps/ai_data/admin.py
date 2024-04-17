from django.contrib import admin
from .models import AiQuestion, AiAnswer, Count

# Register your models here.

class AiAnswerInlnline(admin.TabularInline):
    model = AiAnswer
    extra = 1

@admin.register(AiQuestion)
class AiQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    list_filter = ('user', 'created')
    search_fields = ('user', 'created')
    fieldsets = [
        (None, {'fields': ('user',)}),
        ('주요내용', {'fields': ('question',)}),
    ]
    
    inlines = [AiAnswerInlnline,]
    
@admin.register(AiAnswer)
class AiAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    fieldsets = [
        (None, {'fields': ('user',)}),
        ('주요내용', {'fields': ('question', 'answer')}),
    ]
    
@admin.register(Count)
class ConutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question_count', 'answer_count')