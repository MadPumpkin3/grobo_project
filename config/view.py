from django.views.generic import ListView
from myapps.users.models import User

class Index(ListView):
    template_name = 'index.html' # 사용할 템플릿 파일 지정
    model = User
    
    def get_context_data(self, **kwargs): # **kwargs : Index 클래스에서 받은 request객체를 받는다.
        context = super().get_context_data(**kwargs)
        context['text'] = 'Hellow, Grobo!'
        return context