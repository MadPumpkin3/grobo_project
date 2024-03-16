from django.db import models


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=255, blank=False, null=False)
    context = models.TextField("내용", blank=True, null=True)
    created = models.DateTimeField("생성일시", auto_now_add=True)
    
    tag = models.ManyToManyField("feeds.HashTag", verbose_name="태그명", related_name="tag_posts")
    
    def __str__(self):
        return self.title
    
class PostImage(models.Model):
    post = models.ForeignKey("Post", verbose_name='포스트', on_delete=models.CASCADE)
    image_url = models.ImageField("포스트 이미지", upload_to="post/image", blank=True, null=True)
    
class PostComment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "Post",
        verbose_name="포스트",
        on_delete=models.CASCADE,
        )
    comment = models.TextField("댓글")
    created = models.DateTimeField("작성일시", auto_now_add=True)