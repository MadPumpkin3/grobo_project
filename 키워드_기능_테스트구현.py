# 검색 문장 = 문장 받기(c와 b를 가지고 만들어진 d를 f에 가져간다.)
# 문자 추출 = c, b, d, f, + ⍺(문자를 여러 개 추출)

# 재귀함수?
from myapps.posts.models import SearchKeyword
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

keywords = ['감자', '고구마', '김치', '햇반', '행복', '잡채', '바나나', '사과', '파인애플', '오랑우탄'] # 실제 인덱스는 0~9


class RelatedKeywords():
    
    def __init__(self, keywords):
        self.keywords = keywords
        self.keywords_end = len(keywords) # 종료 조건 기준을 위해 리스트 실제로 들어 있는 요소 갯수 + 1로 설정(할당되는 값은 0 ~ 10 / 인덱스 10은 값이 없음.)
    
    def related_keywords(self, keywords_index = 0):
        # 종료 조건
        if keywords_index == self.keywords_end - 1: # 9 == 9 일 경우, 재귀 중지
            get, created = SearchKeyword.objects.get_or_create(keyword = self.keywords[keywords_index - 1]) # 9번째(마지막)인덱스는 있는지 없는지 여부만 확인
            return keywords_index - 1 # 포커스 값은 8 반환
        
        focus_index = self.related_keywords(keywords_index + 1) # 종료 조건이 충족하지 않으면 현재 인덱스에서 +1로 함수를 호출한다, 종료 조건이 충족되면 8 반환됨
        
        # 재귀함수 종료 이후 실행
        focus_keyword, created = SearchKeyword.objects.get_or_create(keyword = self.keywords[focus_index]) # 8번째 인덱스의 값이 db에 있으면 가져오고 없으면 생성하고 가져오기
        
        for related_index in range(focus_index + 1, self.keywords_end): # range(9, 10) = 9만 호출
            related_keyword = SearchKeyword.objects.get(keyword = self.keywords[related_index]) # 9번째 인덱스의 값 가져오기
            if not focus_keyword.keyword_relation.filter(keyword = related_keyword).exists():
                focus_keyword.keyword.add(related_keyword)
                focus_keyword.save()
            
        return focus_index - 1



# 검색 키워드 데이터 테이블(User 모델과 다대다 관계에서 유저 모델에서만 키워드를 추적할 수 있게 연결되어 있음. / symmetrical=False)
class SearchKeyword(models.Model):
    keyword = models.CharField('검색 키워드', max_length=50)
    # blank=True로 초기 인스턴스 또는 키워드 1개 인스턴스 생성 시, 무한 생성 요청 해결
    keyword_relation = models.ManyToManyField('self', verbose_name='연관 키워드', symmetrical=True, blank=True) 
    count = models.IntegerField('검색 횟수', default=1)
    
    def __str__(self):
        return self.keyword
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("이름", max_length=10, unique=False, null=False, blank=False)
    user_id = models.CharField("아이디", max_length=64, unique=True, null=False)
    password = models.CharField("비밀번호", max_length=255, null=False, blank=False)
    # null은 데이터베이스에서 작동, blank는 폼에서 작동(폼 유효성 검사에 사용)
    email = models.EmailField("이메일", unique=True, null=False, blank=False)
    # 유저의 검색 키워드 저장 필드(유저 쪽에서만 키워드를 추적할 수 있게 설정 / symmetrical=False)
    search_keyword = models.ManyToManyField("posts.SearchKeyword", verbose_name='유저 키워드', related_name='keyword_user', symmetrical=False)