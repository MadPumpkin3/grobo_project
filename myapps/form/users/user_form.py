from django import forms
from myapps.users.models import User
from django.contrib.auth import authenticate
from myapps.common.models import DefaultMainPageChoices

class LoginForm(forms.Form):
    user_id = forms.CharField(
        label='아이디', max_length=64, required=True, widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요.'})
        )
    password = forms.CharField(
        # password 입력시, 입력 값이 보이지 않게 PasswordInput위젯으로 설정
        label='비밀번호', max_length=255, required=True, widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력하세요.'})
        )
    # 로그인 후, 이동하려는 메인 페이지 선택 필드 정의
    default_main_page = forms.IntegerField(
        label='기본 메인 페이지', required=True, widget=forms.RadioSelect(choices=DefaultMainPageChoices.choices)
    )
    
    def clean(self):
        # cleaned_data는 딕셔너리이다.
        # clean_필드명()으로 개별 검사를 하지 않았기 때문에 '유효성 검사'가 진행되지 않아서, super().clean()으로 직접 실행해서 cleaned_data를 확보한다.
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        default_main_page = cleaned_data.get('default_main_page')
        
        # authenticate: 사용자 인증을 하는데 사용, 인증되면 해당 객체를 반환, 실패하면 None을 반환
        user = authenticate(user_id=user_id, password=password)
        
        if not user:
            raise forms.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")
        
        cleaned_data['user'] = user
        cleaned_data['default_main_page'] = default_main_page
        return cleaned_data
    
        # try:
        #     User.objects.get(user_id = user_id)
        # except User.DoesNotExist:
        #     raise forms.ValidationError("해당 아이디는 존재하지 않습니다.")
        
        # # authenticate는 사용자 인증을 확인하기 위해 사용된다. 제공된 id와 password를 가지고 인증한다. 
        # # 인증되면 해당 사용자 객체를 반환하고, 실패하면 None을 반환한다.
        # if not authenticate(user_id=user_id, password=password):
        #     raise ValueError("비밀번호가 일치하지 않습니다.")
    
# password 재확인을 위해 User모델에 없는 password2필드를 생성하는 과정에서 Form클래스가 적합하다고 판단
class JoinForm(forms.Form):
    username = forms.CharField(
        label='이름', max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': '이름을 입력하세요.'})
        )
    user_id = forms.CharField(
        label='아이디', max_length=64, widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요.'})
        )
    password1 = forms.CharField(
        label='비밀번호', max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': '비밀번호를 입력하세요.'})
        )
    password2 = forms.CharField(
        label='비밀번호 확인', max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': '비밀번호를 재입력하세요.'})
        )
    email = forms.EmailField(
        label='이메일', widget=forms.TextInput(attrs={'placeholder': 'abcd@google.com'})
        )
    # ImageField여서 위젯으로 FileInput을 사용했다.
    profile_image = forms.ImageField(
        label='프로필 이미지', required=False, widget=forms.FileInput(attrs={'placeholder': '선택사항입니다.'})
        )
    # 위젯을 textarea로 설정해서 장문의 글이 들어갈 수 있도록 수정(label과 required의 인수를 사용할 수 있도록 charfield 사용)
    short_description = forms.CharField(
        label='소개글', 
        required=False,
        widget=forms.Textarea(attrs={'placeholder': '선택사항입니다.'})
        )
    # 회원가입 시, 기본 메인 페이지 설정 필드
    default_main_page = forms.IntegerField(
        label='기본 메인 페이지',
        required=True,
        widget=forms.RadioSelect(choices=DefaultMainPageChoices.choices)
    )

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        
        if not user_id:
            raise forms.ValidationError('아이디를 입력하세요.')
        
        if User.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError('이미 가입된 아이디입니다.')
        
        return user_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise forms.ValidationError('이메일을 입력해주세요.')
        
        # 해당 이메일이 있는지 필터로 확인하고, exists()메서드로 결과 여부에 따라 불형식(True, False)로 반환한다.
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 가입된 이메일입니다.')
        
        return email
    
    # password1필드와 password2필드 2개의 필드를 비교하기 때문에 개별 유효성 검사는 불가능하여 clean()메서드로 정의
    # clean_필드명()이 실행되면서 '유효성 검사'도 같이 실행되어 cleaned_data가 자동 생성된다.
    # 그러면, 이미 생성된 cleaned_data를 clean()에서 self.cleaned_data.get로 활용할 수 있다.
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or not password2:
            raise forms.ValidationError('비밀번호를 입력해주세요.')
        elif password1 != password2:
            raise forms.ValidationError('비밀번호가 다릅니다.')
   
# password 재확인을 위해 User모델에 없는 password2필드를 생성하는 과정에서 ModelForm클래스는 사용할 수 없다고 판단     
# class JoinForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'user_id', 'password', 'password2', 'email', 'profile_image', 'short_description']
#         widgets = {
#             'username': forms.CharField(
#                 widget=forms.TextInput(attrs={'placeholder': '이름을 입력하세요.'})
#                 ),
#             'user_id': forms.CharField(
#                 widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요.'})
#                 ),
#             'password': forms.CharField(
#                 widget=forms.TextInput(attrs={'placeholder': '비밀번호를 입력하세요.'})
#                 ),
#             'password2': forms.CharField(
#                 widget=forms.TextInput(attrs={'placeholder': '비밀번호를 재입력하세요.'})
#                 ),
#             'email': forms.EmailField(
#                 widget=forms.TextInput(attrs={'placeholder': 'abcd@google.com'})
#                 ),
#             # ImageField여서 위젯으로 FileInput을 사용했다.
#             'profile_image': forms.ImageField(
#                 widget=forms.FileInput(attrs={'placeholder': '선택사항입니다.'})
#                 ),
#             # 위젯을 textarea로 설정해서 장문의 글이 들어갈 수 있도록 수정
#             'short_description': forms.CharField(
#                 widget=forms.Textarea(attrs={'placeholder': '선택사항입니다.'})
#             ),
#         }