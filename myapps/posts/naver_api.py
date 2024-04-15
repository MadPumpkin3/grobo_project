import os
import sys
import urllib.request
import json
from myapps.users.models import User

# 네이버 api 실행 클래스
class NaverSearchAPI():
    
    def __init__(self, keywords):
        self.client_id = "Hg_vYawShJasVfnbKDdB"
        self.client_secret = "b3Eszn4R8y"
        self.data_number = 3
        
    # 검색 실행 시, 검색 api를 요청하는 메서드
    def search_api_start(self, search_text):
        service_list = ["news", "encyc", "webkr"]
        data_number = 3 # 응답 받은 데이터 중, 사용하려는 데이터 갯수
        
        # search_text로 받아온 텍스트의 띄어쓰기를 '+'로 변환
        
        for keyword in keyword_list:
            encText = urllib.parse.quote(keyword)
            for service in service_list:
                search_data, getcode = self.naver_search_api(encText, service, data_number)
                if getcode:
                    search_data
                else:
                    error_text = search_data
                    return error_text
            
    # 사용자 키워드 알고리즘 메서드(사용자가 자주 쓰는 키워드로 뉴스 및 쇼핑 검색 api 요청)
    def algorithms_api_start(self, user_pk):
        service_list = ["news", "shop"]
        user_data = User.objects.get(pk=user_pk)
        user_keyword = user_data.search_keyword[-4:]
        # user 객체를 통해서 user 키워드 불러오기
        
        for keyword in self.keyword_list:
            encText = urllib.parse.quote(keyword)
            for service in service_list:
                search_data, getcode = self.naver_search_api(encText, service)
                if getcode:
                    search_data
                else:
                    error_text = search_data
                    return error_text
    
    # 네이버 api 서버에 요청을 보내는 메서드(응답은 JSON 문자열로 오기 때문에 python객체로 변환이 필요하다.)
    def naver_search_api(self, encText, service, data_number):
        url = f"https://openapi.naver.com/v1/search/{service}?query=" + encText # JSON 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode() # getcode()메서드 : HTTP 응답 코드를 반환한다. (성공적이면 200 반환, 실패하면 오류 코드 반환)
        if(rescode==200):
            # .read()메서드 : HTTP응답의 본문을 읽어들이는 메서드
            # .decode()메서드 : naver_api는 응답이 바이트 형식으로 오는데 그것을 유니코드 문자열로 디코딩하기 위해서 사용
            response_body = response.read().decode('utf-8')
            response_data = json.loads(response_body) # JSON 문자열을 파이썬 객체로 변환
            search_data = response_data['items'][0:data_number] # 'items'의 키의 값 중 일부를 가져온다.
            return search_data, True
        else:
            error_code = "Error Code:" + rescode
            return error_code, False