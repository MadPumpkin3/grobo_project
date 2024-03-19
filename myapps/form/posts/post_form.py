from django import forms
from myapps.posts.models import Post, PostImage, PostComment
from myapps.form.custom_form import MultiFileField

# 중요: view에서 'PostCreateForm'과 'PostImageForm'이 하나의 폼처럼 나오게 작업해야함.
# 작업: PostImageFormset = formset_factory(PostImage, form=PostImageForm, extra=1)
# view에서 폼 생성시, 'PostCreateForm'를 먼저 호출하고, 그 뒤에 'PostImageFormset'를 호출해서 'form=PostImageForm'연결시키기

# 포스트 생성 폼
class PostCreateForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'context', 'tag']
        widgets = {
            'title': forms.CharField(widget=forms.TextInput(attrs={"placeholder": "제목을 입력하세요."})),
            'context': forms.Textarea(attrs={"placeholder": "내용을 입력하세요."}),
            'tag': forms.CharField(widget=forms.TextInput(attrs={"placeholder": "#으로 태그를 구분해서 입력하세요"})),
        }
    
    # '#'으로 받은 '태그'데이터들을 각 객체로 분리하는 과정
    def clean_tag(self):
        tag_data = self.cleaned_data.get('tag')
        
        # 태그 입력 여부 확인
        if tag_data:
            # 입력된 태그 문자열을 '#'기준으로 객체를 분할하고, tag.strip()으로 공백을 없앤 다음 데이터가 있는지 없는지 검사 후, 
            # 데이터가 있으면 strip()을 실행해서 공백 없는 단어만 반환
            # 중요 - if tag.strip() 문은 strip()을 했을 때 공백 여부를 판단만 하는거지 실제로 strip()메서드를 실행하지는 않는다.
            tags = [tag.strip() for tag in tag_data.split('#') if tag.strip()]
            # 분리된 각 tag를 리스트 형태인 tags로 반환(view)에 참고해서 db에 넣기
            return tags

# 포스트 이미지 생성 폼   
class PostImageForm(forms.Form):
    # 여려개의 이미지 파일을 받기 위해 MultiFileField클래스를 만들었음.
    image_url = MultiFileField(label='이미지', required=False, 
                               # ClearableFileInput : 파일 입력 필드에 파일을 선택하거나 현재 선택된 파일을 지울 수 있는 클리어 버튼을 제공
                               widget=forms.ClearableFileInput(attrs={'placeholder': '선택사항입니다.', 'multiple': True}))

# 포스트 댓글 생성 폼
class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(attrs={"placeholder": "댓글을 입력하세요."}),
        }