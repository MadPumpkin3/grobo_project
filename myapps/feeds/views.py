from typing import Any
from django.shortcuts import render
from django.views import generic
from .models import Feed, FeedComment

# Create your views here.

class Platform_main(generic.ListView):
    template_name = 'feeds/platform_main.html'
    model = Feed
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'Platform_main view 테스트용'
        return context