from django import forms

# 여러개의 파일을 받는 사용자 정의 필드
class MultiFileField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FileField(),
        )
        super().__init__(fields, *args, **kwargs)
    
    # compress는 폼에서 전송된 데이터를 압축하고 유효성 검사를 수행하는데 사용된다.
    # 그러나 현재 유효성 검사에 대한 처리 코드가 없어서, 처리 코드를 compress메서드에 직접 추가해줘야 한다.
    # data_list는 리스트 형태로 제공된다.
    def compress(self, data_list):
        if data_list:
            image_urls = [image.strip() for image in data_list if image.strip()]
            return image_urls