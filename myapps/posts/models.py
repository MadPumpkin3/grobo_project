from django.db import models
from markdownx.models import MarkdownxField
from markdownx.widgets import MarkdownxWidget

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=255, blank=False, null=False)
    content = MarkdownxField("내용", blank=True, null=True)
    created = models.DateTimeField("생성일시", auto_now_add=True)
    
    tag = models.ManyToManyField("feeds.HashTag", verbose_name="태그명", related_name="tag_posts", blank=True)
    
    def __str__(self):
        return self.title
    
# 미리보기 포스트 이미지와 완성된 포스트 이미지를 갖는 테이블(유연한 ForeignKey 전환을 위해 2개의 키를 할당)
class PostImage(models.Model):
    post = models.ForeignKey("Post", verbose_name='포스트 이미지', blank=True, null=True, on_delete=models.CASCADE)
    # preview_post랑 연결된 'PreviewPost' 객체가 삭제될 때, 이미지가 같이 삭제되지 않고 None 로 바뀌게 설정('PreviewPost' 객체는 사용자가 포스트 저장시 자동 삭제될 예정)
    preview_post = models.ForeignKey('PreviewPost', verbose_name='미리보기 이미지', blank=True, null=True, on_delete=models.SET_NULL)
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

# 포스트 미리보기용 데이터 테이블(임시 보관용 테이블)
class PreviewPost(models.Model):
    user = models.ForeignKey('users.User', verbose_name='작성자', on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=255, blank=True, null=True)
    content = MarkdownxField('내용', blank=True, null=True)
    tag = models.CharField('태그', max_length=255, blank=True, null=True)
    created = models.DateTimeField('생성일시', auto_now_add=True)