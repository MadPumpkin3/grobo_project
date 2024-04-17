from django import template
# mark_safe 함수는 HTML을 안전하게 표시할 때 사용됩니다.
from django.utils.safestring import mark_safe
# markdownify 필터는 마크다운 형식의 텍스트를 HTML로 변환할 수 있습니다.
from markdownx.utils import markdownify, markdown

# posts 전용 사용자 정의 필터 생성

register = template.Library()

# 마크다운으로 입력된 텍스트를 렌더링 후, 미리보기 형식으로 보여줄 때 '마크다운'코드가 적용될 수 있게 '이스케이핑'을 우회하여 적용하는 필터
# 렌더링 가능 범위 : 마크다운 텍스트 가능, HTML 코드 가능(HTML 코드까지 렌더링이 가능하기 때문에 보완에 중요)
@register.filter(name='formatted_markdown')
def formatted_markdown(text):
    return mark_safe(markdownify(text))

# 렌더링 가능 범위 : 마크다운 텍스트 가능, HTML 코드 불가능
# @register.filter(name='formatted_markdown')
# def formatted_markdown(text):
#     return markdown(text)