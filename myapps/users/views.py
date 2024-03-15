from django.shortcuts import render
from django.views.generic import FormView
from .models import User

# Create your views here.

class Login(FormView):
    template_name = 'users/login.html'
    model = User