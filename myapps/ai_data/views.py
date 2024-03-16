from django.shortcuts import render
from django.views import generic
from .models import AiQuestion, AiAnswer

# Create your views here.

class AiMain(generic.ListView):
    template_name = 'ai_data/ai_main.html'
    model = AiQuestion
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'AiMain view 테스트용'
        return context