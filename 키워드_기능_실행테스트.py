from konlpy.tag import Kkma
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from django.views import generic

# 클래스 뷰 형태의 테스트 클래스 생성
# class KeywordsExtraction(generic.TemplateView):
#     template_name = 'posts/portal_search_results.html'
    
#     kkma = Kkma()
  
# 단순 입력 형태의 테스트 클래스 생성  
# class TestKeywordsExtraction():
    
#     kkma = Kkma() # 한국어 형태소 분석기 초기화
    
#     text = input('문장을 입력해주세요.: ')
#     korean_result = kkma.pos(text) # .pos()메서드: 주어진 한국어 문장을 형태소 단위로 분리하고, 품사 정보도 함께 반환(리스트[(형태소, 품사),]
#     english_tokens = word_tokenize(text)
#     english_result = pos_tag(english_tokens)
    
#     print('한국어 형태소: ', korean_result)
#     print('영어 형태소: ', english_result)
    
# 영단어 판독 코드
def english_words_reader(english_nouns):
    english_word_list = []

    for word in english_nouns:
        if word.encode().isalpha():
            english_word_list.append(word)
        
    return english_word_list


kkma = Kkma() # 한국어 형태소 분석기 초기화

text = input('문장을 입력해주세요.: ')
korean_result = kkma.pos(text) # .pos()메서드: 주어진 한국어 문장을 형태소 단위로 분리하고, 품사 정보도 함께 반환(리스트[(형태소, 품사),]
korean_nouns = [word for word, pos in korean_result if pos.startswith('N')] # 단어만 추출
english_tokens = word_tokenize(text)
english_result = pos_tag(english_tokens)
english_nouns = [word for word, pos in english_result if pos.startswith('N')] # 명사만 추출(일반 명사, 대명사, 단수, 복수 포함)
english_words = english_words_reader(english_nouns)

print('한국어 형태소: ', korean_nouns)
print('영어 형태소: ', english_words)

# class RelatedKeywords():
    
#     def __init__(self, keywords):
#         self.keywords = keywords
#         self.keywords_end = len(keywords) # 종료 조건 기준을 위해 리스트 실제로 들어 있는 요소 갯수 + 1로 설정(할당되는 값은 0 ~ 10 / 인덱스 10은 값이 없음.)
    
#     def related_keywords(self, keywords_index = 0):
#         # 종료 조건
#         if keywords_index == self.keywords_end - 1: # 9 == 9 일 경우, 재귀 중지
#             get, created = SearchKeyword.objects.get_or_create(keyword = self.keywords[keywords_index - 1]) # 9번째(마지막)인덱스는 있는지 없는지 여부만 확인
#             return keywords_index - 1 # 포커스 값은 8 반환
        
#         focus_index = self.related_keywords(keywords_index + 1) # 종료 조건이 충족하지 않으면 현재 인덱스에서 +1로 함수를 호출한다, 종료 조건이 충족되면 8 반환됨
        
#         # 재귀함수 종료 이후 실행
#         focus_keyword, created = SearchKeyword.objects.get_or_create(keyword = self.keywords[focus_index]) # 8번째 인덱스의 값이 db에 있으면 가져오고 없으면 생성하고 가져오기
        
#         for related_index in range(focus_index + 1, self.keywords_end): # range(9, 10) = 9만 호출
#             related_keyword = SearchKeyword.objects.get(keyword = self.keywords[related_index]) # 9번째 인덱스의 값 가져오기
#             if not focus_keyword.keyword_relation.filter(keyword = related_keyword).exists():
#                 focus_keyword.keyword.add(related_keyword)
#                 focus_keyword.save()
            
#         return focus_index - 1