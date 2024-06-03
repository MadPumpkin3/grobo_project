import json
import asyncio
import aiohttp
from asgiref.sync import sync_to_async
import urllib.request
from urllib.parse import quote
from konlpy.tag import Kkma # 한국어 형태소 라이브러리로 단어와 품사로 구분하여 반환하기 위해 호출
from nltk.tokenize import word_tokenize # 영어 형태소 라이브러리로 영어를 토큰화 하기 위해 호출
from nltk.tag import pos_tag # 영어 형태소 라이브러리로 단어와 품사로 구분하여 반환하기 위해 호출
from django.views import generic
from django.utils import timezone
from myapps.posts.models import SearchKeyword
from myapps.users.models import UserSearchKeyword, User

# 네이버 api 실행 클래스
class NaverSearchAPI():
    
    def __init__(self):
        self.client_id = "Hg_vYawShJasVfnbKDdB" # 네이버 API 사용을 위한 인증 id
        self.client_secret = "b3Eszn4R8y" # 네이버 API 사용을 위한 인증 pw
        self.search_service_list = ["news", "encyc", "webkr"] # 검색 결과 요청하려는 서비스
        self.search_number_responses = 4 # 검색 결과 데이터의 서비스별 갯수
        self.algorithms_service_list = ["news", "shop", "blog"] # 알고리즘 결과 요청하려는 서비스
        self.algorithms_number_responses = 1 # 알고리즘 데이터의 서비스별 갯수
        
    # 검색 실행 시, 검색 api를 요청하는 메서드
    async def search_api_request(self, transformed_text):
        encText = quote(transformed_text) # 네이버 API url로 전송을 위해 텍스트를 인코딩
        number_response = self.search_number_responses # 검색 결과 데이터의 서비스별 갯수 가져오기
        search_results_list = {} # 반환할 딕셔너리 변수 초기화
        
        for service in self.search_service_list:
            search_data, getcode = await self.naver_search_api(encText, service, number_response) # 네이버 API 요청 함수에 위 인수를 넣어 실행
            if getcode:
                search_results_list[service] = search_data # 서비스을 키로 갖는 'API 응답 중 데이터'를 값으로 넣는다.
            else:
                search_results_list[service] = search_data # 에러 메세지가 포함됨.
        
        return search_results_list # 서비스명(key)에 따라 반환된 API 결과 값(value)을 갖는 '중첩된 딕셔너리와 리스트' 변수를 반환
        
    # 동기적 기능 코드
    # 네이버 api 서버에 요청을 보내는 메서드(응답은 JSON 문자열로 오기 때문에 python객체로 변환이 필요하다.)
    async def naver_search_api(self, encText, service, number_responses):
        url = f"https://openapi.naver.com/v1/search/{service}?query=" + encText # JSON 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request) # urllib.request : 동기 API 요청 코드
        rescode = response.getcode() # getcode()메서드 : HTTP 응답 코드를 반환한다. (성공적이면 200 반환, 실패하면 오류 코드 반환)
        if(rescode==200):
            # .read()메서드 : HTTP응답의 본문을 읽어들이는 메서드
            # .decode()메서드 : naver_api는 응답이 바이트 형식으로 오는데 그것을 유니코드 문자열로 디코딩하기 위해서 사용
            response_body = response.read().decode('utf-8')
            response_data = json.loads(response_body) # JSON 문자열을 파이썬 객체로 변환
            search_data = response_data['items'][0:number_responses] # 'items'의 키의 값 중 일부를 가져온다.
            return search_data, True
        else:
            error_code = "Error Code:" + rescode
            return error_code, False
        
    # 사용자 키워드 알고리즘 메서드(사용자가 자주 쓰는 키워드로 뉴스 및 쇼핑 검색 api 요청)
    async def algorithms_api_request(self, user):
        number_response = self.algorithms_number_responses
        search_results_list = {} # 반환할 딕셔너리 변수 초기화
        
        # 사용자 로그인 여부에 따라 키워드 추출 모델 변경
        if user.is_authenticated:
            user_keyword_list = UserSearchKeyword.objects.filter(user = user)[:3] # 모델에 내림차순으로 설정되어 있어서 상위 3개만 가져오면 됨.
            enctext_list = [user_keyword.search_keyword for user_keyword in user_keyword_list] # 상위 3개의 객체에서 키워드만 추출
        else:
            db_keyword_list = SearchKeyword.objects.filter()[:3] # 모델에 내림차순으로 설정되어 있어서 상위 3개만 가져오면 됨.
            enctext_list = [db_keyword.keyword for db_keyword in db_keyword_list] # 상위 3개의 객체에서 키워드만 추출
        
        for service in self.algorithms_service_list: # 서비스별로 api 요청 호출
            for encText in enctext_list: # 키워드별로 api 요청 호출
                search_data, getcode = await self.naver_search_api(encText, service, number_response) # 네이버 API 실행 함수에 위 인수를 넣어 실행 
                if getcode:
                    search_results_list[service] = search_data # 서비스을 키로 갖는 'API 응답 중 데이터'를 값으로 넣는다.
                else:
                    search_results_list[service] = search_data # 에러 메세지가 포함됨
        
        return search_results_list # 서비스명(key)에 따라 반환된 API 결과 값(value)을 갖는 '중첩된 딕셔너리와 리스트' 변수를 반환
        
# 텍스트를 API url 텍스트로 변환하는 함수(공백을 '+'로 변경)
def text_transform(text):
    text_strip = text.strip() # 문장 양쪽 끝 공백 제거
    transformed_text = text_strip.replace(' ', '+') # replace() 메서드: 특정 문자열을 다른 문자열로 대체한다.
    return transformed_text
    
# 텍스트에서 키워드를 추출하는 클래스
class TextKeywordReader():
    
    def __init__(self, text):
        self.text = text
    
    # 검색어에 한국어 단어와 영어 단어 추출(전처리)
    def text_keyword_reader(self):
        kkma = Kkma() # 한국어 형태소 분석기 초기화
        
        # 한국어 단어 추출 코드
        korean_result = kkma.pos(self.text) # .pos()메서드: 주어진 한국어 문장을 형태소 단위로 분리하고, 품사 정보도 함께 반환(리스트[(형태소, 품사),]
        korean_words = []
        for word, pos in korean_result: # 키워드와 품사 추출
            if pos.startswith('N') and not word in korean_words: # 중복되지 않는 한국어 단어 추출
                korean_words.append(word)
        
        # 영어 단어 추출 코드
        english_tokens = word_tokenize(self.text)
        english_result = pos_tag(english_tokens)
        english_nouns = []
        for word, pos in english_result: # 키워드와 품사 추출
            if pos.startswith('N') and not word in english_nouns: # 중복되지 않는 명사 추출(일반 명사, 대명사, 단수, 복수 포함)
                english_nouns.append(word)
        english_words = self.english_words_reader(english_nouns)
        
        keywords = korean_words + english_words
        
        return keywords

    # 영단어 판독 코드(nltk라이브러리는 한국어를 걸러내지 못해서 직접 걸러내는 메서드 실행)(전처리)
    def english_words_reader(self, english_nouns):
        english_word_list = []

        for word in english_nouns:
            if word.encode().isalpha():
                english_word_list.append(word)
            
        return english_word_list    

# 추출된 키워드를 'SearchKeyword' 테이블과 'UserSearchKeyword' 테이블에 저장하는 클래스(이중 연결 리스트)
class Keyword_save():
    def __init__(self, user, keyword_list):
        self.user = user
        self.keyword_list = keyword_list
    
    # 키워드를 DB에 있는 SearchKeyword와 User 테이블에 저장하는 메서드
    def keyword_save(self):
        user_yn = self.user.is_authenticated # 유저 로그인 여부를 bool로 반환 후, 변수에 할당
        
        # 키워드 리스트에서 첫 번째 키워드 가져오기 또는 생성 후 가져오기
        zero_keyword_get, zero_keyword_create = SearchKeyword.objects.get_or_create(keyword = self.keyword_list[0])
        if not zero_keyword_create: # 기존에 있던 객체라면 count 속성에 1 더하기(모든 사용자들의 관심도 파악)
            zero_keyword_get.count += 1
            zero_keyword_get.save()
            
        if user_yn:
            user_zero_keyword_filter = UserSearchKeyword.objects.filter(user = self.user, search_keyword = zero_keyword_get)
            if user_zero_keyword_filter.exists():
                user_first_keyword = UserSearchKeyword.objects.get(user = self.user, search_keyword = zero_keyword_get)
                user_first_keyword.get_at = timezone.now()
                user_first_keyword.save()
            else:
                user_first_keyword = UserSearchKeyword.objects.create(user = self.user, get_at = timezone.now())
                user_first_keyword.search_keyword.add(zero_keyword_get)
        
        # 키워드가 2개 이상일 경우 실행
        if len(self.keyword_list) > 1:
            
            # 첫 번째 키워드를 사용 목적의 변수생성 및 값 할당
            related_keyword = zero_keyword_get # SearchKeyword 테이블의 다대다 필드 객체인 related 키워드 할당용 변수
            
            # SearchKeyword 테이블에 객체 생성 및 다대다 필드 연결
            for index in range(1, len(self.keyword_list)): # keyword_list[n] 객체와 keyword_list[n-1] 객체의 연결성을 확인하기 위해 1부터 시작
                focus_keyword, focus_keyword_create = SearchKeyword.objects.get_or_create(keyword = self.keyword_list[index])
                
                if not focus_keyword_create: # 기존에 있던 객체라면 count 속성에 1 더하기(모든 사용자들의 관심도 파악)
                    focus_keyword.count += 1
                
                # 현재 포커스 키워드에 이전 키워드(포커스 키워드 인덱스 - 1)가 관계 키워드가 아닐 경우, 관계 키워드로 저장 진행
                if not focus_keyword.keyword_relation.filter(keyword = related_keyword).exists():
                    focus_keyword.keyword_relation.add(related_keyword)
                
                focus_keyword.save()
                
                related_keyword = focus_keyword # DB 접근 최소화를 위해 현재 focus 키워드를 related 키워드에 넣어서 다음 focus 키워드가 사용할 수 있게 활용
                
                # 유저가 로그인 했으면, UserSearchKeyword 테이블에 객체 생성 및 다대다 필드 연결
                if user_yn:
                    user_keyword_filter = UserSearchKeyword.objects.filter(user = self.user, search_keyword = focus_keyword)
                    if user_keyword_filter.exists(): # 기존에 있던 객체라면 data_time 필드인 'get_at'를 현재 일시로 변경
                        user_keyword = UserSearchKeyword.objects.get(user = self.user, search_keyword = focus_keyword)
                        user_keyword.get_at = timezone.now()
                        user_keyword.save()
                    else:
                        user_keyword = UserSearchKeyword.objects.create(user = self.user, get_at = timezone.now())
                        user_keyword.search_keyword.add(focus_keyword)
            
            # 키워드 리스트의 첫 번째 키워드와 마지막 키워드를 연결(1개인 경우 실행 안 함)
            if not zero_keyword_get.keyword_relation.filter(keyword = focus_keyword).exists():
                zero_keyword_get.keyword_relation.add(focus_keyword)