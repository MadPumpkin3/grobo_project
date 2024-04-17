from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# superuser(관리자 계정)생성을 위한 모델
class UserManager(BaseUserManager):
    # 유저를 생성하는 메서드 입니다.
    # **extra_fields 매개변수로 폼에 입력된 기타 값들을 불러옵니다.
    def create_user(self, user_id, email, password=None, **extra_fields):
        if not user_id:
            raise ValueError("유저 id가 없습니다.")
        user = self.model(
            user_id=user_id,
            # normalize_email : @뒤의 도메인 부분을 소문자로 바꿔주는 함수
            email=self.normalize_email(email),
            **extra_fields
            )
        # 비밀번호를 안전하게 저장하기 위해 set_password로 해싱하여 저장한다.
        user.set_password(password)
        # using은 특정 데이터베이스를 지정, self._db는 UserManager클래스이 사용하는 데이터베이스를 나타냄.
        # 즉, UserManager클래스가 사용하는 데이터베이스를 지정하여 거기에 저장한다는 말이다.
        user.save(using=self._db)
        return user
    
    # 관리자를 생성하는 메서드 입니다.
    # **extra_fields 매개변수로 폼에 입력된 기타 값들을 불러옵니다.
    def create_superuser(self, user_id, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # 관리자 계정 생성시 기본 세팅 값들이 True가 아닐 때, 오류 생성
        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자 계정의 staff 필드 값이 True가 아닙니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자 계정의 superuser 필드 값이 True가 아닙니다.')
        
        # 관리자용 계정으로 세팅된 데이터들을 기본 유저 생성 메서드로 실행        
        return self.create_user(user_id, email, password, **extra_fields)

# 유저 모델(유저 테이블)
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("이름", max_length=10, unique=False, null=False, blank=False)
    user_id = models.CharField("아이디", max_length=64, unique=True, null=False)
    password = models.CharField("비밀번호", max_length=255, null=False, blank=False)
    # null은 데이터베이스에서 작동, blank는 폼에서 작동(폼 유효성 검사에 사용)
    email = models.EmailField("이메일", unique=True, null=False, blank=False)
    # 크롬 브라우저의 버전 문제로 파일 업로드 기능이 안될 수 있다. 안돼면 크롬 업데이트를 진행하자
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
    # 유저가 로그인 시, 포털 사이트(값:None) 또는 플랫폼 사이트(값:1)에 따라 이동할 수 있도록 필드 추가
    # 데이터 입력 조건을 0 ~ 1로 제한
    # 코드의 가독성과 명확성을 위해 bool형식으로도 할 수 있지만, 저장공간과 검색 성능 향상을 위해 0,1로만 작업
    default_main_page = models.IntegerField(
        "기본 메인 페이지", 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
        )
    
    # superuser(관리자 계정)생성을 위해 UserManager모델 연결
    objects = UserManager()
    
    # 포스트와 피드의 좋아요 필드
    # blank=True를 지정하지 않으면, 관리자 페이지에서 필수 입력 항목으로 지정되어 저장이 안된다.
    like_posts = models.ManyToManyField("posts.Post", verbose_name="좋아요한 포스트", related_name="like_post_users", blank=True)
    like_feeds = models.ManyToManyField("feeds.Feed", verbose_name="좋아요한 피드", related_name="like_feed_users", blank=True)
    
    following = models.ManyToManyField(
        'self',
        verbose_name="내가 팔로잉한 사람들",
        related_name="followers",
        # a,d,e유저가 b유저를 팔로잉(일방적인 친추)을 했다는 전제하에, b.followers.all()를 호출하면 b유저를 기준으로 b를 팔로잉한 모든 유저가 반환된다.
        symmetrical= False, # symmetrical: 대칭 관계 여부를 정하는 속성으로 기본적으로 a가 b를 가지고 있다면 b도 a를 갖는다.(기본값 True)
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
    
# 사용자 검색 키워드 테이블
class UserSearchKeyword(models.Model):
    user = models.ForeignKey('User', verbose_name='사용자', on_delete=models.CASCADE)
    # 유저의 검색 키워드 저장 필드(유저 쪽에서만 키워드를 추적할 수 있게 설정 / symmetrical=False)
    search_keyword = models.ManyToManyField("posts.SearchKeyword", verbose_name='사용자 검색 키워드', related_name='keyword_user', symmetrical=False, blank=True)
    get_at = models.DateTimeField("최근 조회 일시", auto_now_add=True, blank=True) # 사용자가 해당 객체를 부를 때마다 시간이 업데이트 된다.
    
    # 오류로 인해 사용 중지
    # def __str__(self):
    #     return self.search_keyword
    
    class Meta:
        ordering = ['-get_at'] # 사용자가 최근에 검색한 키워드를 가져오기 위해 내림차순으로 설정