from django.db import models

# Create your models here.

class AiQuestion(models.Model):
    user = models.ForeignKey("users.User", verbose_name="질문자", on_delete=models.CASCADE)
    question = models.TextField("질문", blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    
class AiAnswer(models.Model):
    user = models.ForeignKey("users.User", verbose_name="답변자", on_delete=models.CASCADE)
    question = models.ForeignKey("ai_data.AiQuestion", verbose_name="질문", on_delete=models.CASCADE)
    answer = models.TextField("답변", blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    
class Count(models.Model):
    user = models.ForeignKey("users.User", verbose_name="사용자", on_delete=models.CASCADE)
    question_count = models.IntegerField("질문 작성 횟수", default=2)
    answer_count = models.IntegerField("답변 작성 횟수", default=1)
    