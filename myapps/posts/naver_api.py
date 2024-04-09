import os
import sys
import urllib.request

# 네이버 api 실행 클래스
class NaverSearchAPI():
    client_id = "Hg_vYawShJasVfnbKDdB"
    client_secret = "b3Eszn4R8y"
    encText = urllib.parse.quote("백종원")
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read() # read()메서드 : HTTP응답의 본문을 읽어들이는 메서드
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)