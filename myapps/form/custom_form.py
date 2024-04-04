from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

# 여러개의 파일을 받는 사용자 정의 필드 - 현재 미사용 (사유: 템플릿에 input의 multiple 속성으로 구현)
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
        
# 이미지 유효성 검사(Pillow 라이브러리 활용)
def validate_image(image):
    # 파일의 확장자를 확인하여 이미지 파일인지 확인합니다.
    if not image.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return False, '이미지 파일만 업로드 할 수 있습니다.' # 유효성 검사에 실패하면 뷰에서 판단할 수 있게 False와 오류 메세지를 전달한다.
    
    # 이미지 파일을 열어서 유효한 이미지 파일인지 확인
    try:
        img = Image.open(image)
        img.verify()
    except Exception as e:
        return False, '유효하지 않는 이미지 파일입니다.' # 유효성 검사에 실패하면 뷰에서 판단할 수 있게 False와 오류 메세지를 전달한다.
    
    # 이미지 파일의 크기를 확인하여 허용 가능한 크기 이내인지 확인한다.
    max_size = 5 * 1024 * 1024 # 5MB
    if image.size > max_size:
        return False, '이미지 파일의 크기는 5MB를 넘을 수 없습니다.' # 유효성 검사에 실패하면 뷰에서 판단할 수 있게 False와 오류 메세지를 전달한다.
    
    return True, None # 유효성 검사에 성공하면 뷰에서 판단할 수 있게 True를 전달한다.