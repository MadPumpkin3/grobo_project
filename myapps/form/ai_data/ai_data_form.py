from django import forms
from myapps.ai_data.models import AiQuestion, AiAnswer

# Ai 질문 데이터 폼
class AiQuestionForm(forms.ModelForm):
    
    class Meta:
        model = AiQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'placeholder':'질문을 입력하세요.'})
        }

# Ai 답변 데이터 폼        
class AiAnswerForm(forms.ModelForm):
    
    class Meta:
        model = AiAnswer
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'placeholder':'답변을 입력하세에요.'})
        }