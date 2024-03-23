from django.db import models

# 유저의 기본 메인 페이지 조회 및 변경을 위해 IntegerChoices로 재사용 가능한 선택 목록 정의
class DefaultMainPageChoices(models.IntegerChoices):
    OPTION_ZERO = 0, 'Grobo(포털 페이지)'
    OPTION_ONE = 1, 'Grobat(플랫폼 페이지)'