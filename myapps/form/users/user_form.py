from django import forms
from users.models import User, FollowRelation

class LoginForm(forms.Form):
    user_id = forms.CharField(
        label='아이디', max_length=64, required=True, widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요.'})
        )
    password = forms.CharField(
        label='비밀번호', max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': '비밀번호를 입력하세요.'})
        )
    
    def clean(self):
        # cleaned_data는 딕셔너리이다.
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        # user_id로 로그인하는 것이기 때문에 필터도 user_id로 진행
        user_data = User.objects.filter(user_id=cleaned_data['user_id'])
        password_chack = user_data.first().password
        
        # 사용자가 있는지 확인하는 처리도 필요!
        
        if password != password_chack:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
    
class JoinForm(forms.Form):
    username = forms.CharField(
        label='이름', max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': '이름을 입력하세요.'})
        )
    user_id = forms.CharField(
        label='아이디', max_length=64, required=True, widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요.'})
        )
    password1 = forms.CharField(
        label='비밀번호', max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': '비밀번호를 입력하세요.'})
        )
    password2 = forms.CharField(
        label='비밀번호 확인', max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': '비밀번호를 재입력하세요.'})
        )
    email = forms.EmailField(
        label='이메일', required=True, widget=forms.TextInput(attrs={'placeholder': 'abcd@google.com'})
        )
    # ImageField여서 위젯으로 FileInput을 사용했다.
    profile_image = forms.ImageField(
        label='프로필 이미지', required=False, widget=forms.FileInput(attrs={'placeholder': '선택사항입니다.'})
        )
    # 위젯을 textarea로 설정해서 장문의 글이 들어갈 수 있도록 수정
    short_description = forms.CharField(
        label='소개글', required=False, widget=forms.Textarea(attrs={'placeholder': '선택사항입니다.'})
    )