# 검색 문장 = 문장 받기(c와 b를 가지고 만들어진 d를 f에 가져간다.)
# 문자 추출 = c, b, d, f, + ⍺(문자를 여러 개 추출)

# 재귀함수?

keywords = ['감자', '고구마', '김치', '햇반', '행복', '잡채', '바나나', '사과', '파인애플', '오랑우탄'] # 실제 인덱스는 0~9

class RelatedKeywords():
    
    def __init__(self, keywords):
        self.keywords = keywords
        self.keywords_end = len(keywords) # 종료 조건 기준을 위해 리스트 실제로 들어 있는 요소 갯수 + 1로 설정(할당되는 값은 0 ~ 10 / 인덱스 10은 값이 없음.)
    
    def related_keywords(self, keywords_index = 0):
        # 종료 조건
        if keywords_index == self.keywords_end - 1: # 9 == 9 일 경우, 재귀 중지
            get, created = SearchKeywords.objects.get_or_create(keyword = self.keywords[keywords_index - 1]) # 9번째(마지막)인덱스는 있는지 없는지 여부만 확인
            return keywords_index - 1 # 포커스 값은 8 반환
        
        focus_index = self.related_keywords(keywords_index + 1) # 종료 조건이 충족하지 않으면 현재 인덱스에서 +1로 함수를 호출한다, 종료 조건이 충족되면 8 반환됨
        
        # 재귀함수 종료 이후 실행
        focus_keyword, created = SearchKeywords.objects.get_or_create(keyword = self.keywords[focus_index]) # 8번째 인덱스의 값이 db에 있으면 가져오고 없으면 생성하고 가져오기
        
        for related_index in range(focus_index + 1, self.keywords_end): # range(9, 10) = 9만 호출
            related_keyword = SearchKeywords.objects.get(keyword = self.keywords[related_index]) # 9번째 인덱스의 값 가져오기
            if not focus_keyword.keyword_relation.filter(keyword = related_keyword).exists():
                focus_keyword.keyword.add(related_keyword)
                focus_keyword.save()
            
        return focus_index - 1