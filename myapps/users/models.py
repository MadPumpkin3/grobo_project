from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

# superuser(관리자 계정)생성을 위한 모델
class UserManager(BaseUserManager):
    # 유저를 생성하는 메서드 입니다.
    def create_user(self, user_id, email, password=None):
        if not user_id:
            raise ValueError("유저 id가 없습니다.")
        user = self.model(
            user_id=user_id,
            # normalize_email : @뒤의 도메인 부분을 소문자로 바꿔주는 함수
            email=self.normalize_email(email),
            )
        # 비밀번호를 안전하게 저장하기 위해 set_password로 해싱하여 저장한다.
        user.set_password(password)
        # using은 특정 데이터베이스를 지정, self._db는 UserManager클래스이 사용하는 데이터베이스를 나타냄.
        # 즉, UserManager클래스가 사용하는 데이터베이스를 지정하여 거기에 저장한다는 말이다.
        user.save(using=self._db)
        return user
    
    # 관리자를 생성하는 메서드 입니다.
    def create_superuser(self, user_id, email, password):
        user = self.create_user(user_id, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# 유저 모델(유저 테이블)
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("이름", max_length=10, unique=False, null=False, blank=False)
    user_id = models.CharField("아이디", max_length=64, unique=True, null=False)
    password = models.CharField("비밀번호", max_length=255, null=False, blank=False)
    # null은 데이터베이스에서 작동, blank는 폼에서 작동(폼 유효성 검사에 사용)
    email = models.EmailField("이메일", unique=True, null=False, blank=False)
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True)
    short_description = models.TextField("소개글", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # created_at, updated_at, login_at은 속성명 자체로 자동처리 기능이 있다.
    # created_at(해당 레코드가 만들어질 때), updated_at(해당 레코드가 업데이트 될 때), login_at(해당 레코드가 로그인 할 때)
    created_at = models.DateTimeField("회원가입 일시", auto_now_add=True, blank=True)
    updated_at = models.DateTimeField("최근 수정 일시", auto_now_add=True, blank=True)
    login_at = models.DateTimeField("최근 로그인 일시", auto_now=True, blank=True, null=True)
    
    # superuser(관리자 계정)생성을 위해 UserManager모델 연결
    objects = UserManager()
    
    # 포스트와 피드의 좋아요 필드
    like_posts = models.ManyToManyField("posts.Post", verbose_name="좋아요한 포스트", related_name="like_post_users")
    like_feeds = models.ManyToManyField("feeds.Feed", verbose_name="좋아요한 피드", related_name="like_feed_users")
    
    following = models.ManyToManyField(
        'self',
        verbose_name="내가 팔로잉한 사람들",
        related_name="followers",
        # a,d,e유저가 b유저를 팔로잉(일방적인 친추)을 했다는 전제하에, b.followers.all()를 호출하면 b유저를 기준으로 b를 팔로잉한 모든 유저가 반환된다.
        symmetrical= False,
        through='users.FollowRelation',
        # 중계형 테이블을 따로 만들지 않을 경우, 자동 생성된다.
        )
    
    # 로그인, 로그아웃에 사용되는 '사용자 인증'시 참조하는 기존 필드를 'username'필드에서 'user_id'필드로 변경하기 위함
    # 즉, 로그인 시 username필드(본명)이 아니라 user_id필드(닉네임)으로 사용자를 인증한다.(판별한다.)
    USERNAME_FIELD = 'user_id'
    # 사용자를 생성할 때(회원가입)할 때, 기본 필수 입력사항(user_id, password) 빼고 필수로 지정하고 싶은 것을 지정하는 것
    REQUIRED_FIELDS = ['email', ]
    
    
    class Meta:
        db_table = 'user_profile'
        
    def __str__(self):
        return self.username
    
# 팔로우 중개 테이블
class FollowRelation(models.Model):
    follow_from = models.ForeignKey(
        "users.User",
        verbose_name = '팔로우 요청한 사용자',
        related_name = 'followers_relation',
        on_delete = models.CASCADE,
        )
    follow_to = models.ForeignKey(
        "users.User",
        verbose_name = '팔로우 요청의 대상',
        related_name = 'following_relation',
        on_delete = models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'관계: {self.follow_from} -> {self.follow_to}' 