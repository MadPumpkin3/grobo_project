from django.db import models

# Create your models here.

class Feed(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    context = models.TextField("내용", blank=True)
    image_url = models.ImageField("피드 이미지", upload_to="feed/image", blank=False, null=False)
    created = models.DateTimeField("작성일시", auto_now_add=True)
    
    tag = models.ManyToManyField("feeds.HashTag", verbose_name="태그명", related_name="tag_feeds")
    
class FeedComment(models.Model):
    user = models.ForeignKey(
        "users.User", 
        verbose_name="작성자", 
        on_delete=models.CASCADE,
        )
    feed = models.ForeignKey(
        "Feed", 
        verbose_name="피드", 
        on_delete=models.CASCADE,
        )
    comment = models.TextField("댓글", blank=False, null=False)
    created = models.DateTimeField("작성일시", auto_now_add=True)
    
class HashTag(models.Model):
    tag_name = models.CharField("태그명", max_length=50)
    
    def __str__(self):
        return self.tag_name
    
    