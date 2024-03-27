from django import forms
from myapps.posts.models import Post, PostImage, PostComment
from myapps.form.custom_form import MultiFileField
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

# 중요: view에서 'PostCreateForm'과 'PostImageForm'이 하나의 폼처럼 나오게 작업해야함.
# 작업: PostImageFormset = formset_factory(PostImage, form=PostImageForm, extra=1)
# view에서 폼 생성시, 'PostCreateForm'를 먼저 호출하고, 그 뒤에 'PostImageFormset'를 호출해서 'form=PostImageForm'연결시키기

# 포스트 생성 폼
class PostCreateForm(forms.Form):
    title = forms.CharField(
        label='제목', max_length=255, required=True, widget=forms.TextInput(attrs={"placeholder": "제목을 입력하세요.", "id": "id_title"})
    )
    content = MarkdownxFormField(
        label='내용', required=True, widget=MarkdownxWidget(attrs={"placeholder": "내용을 입력하세요.", "id": "id_content"})
    )
    tag = forms.CharField(
        label='태그', widget=forms.TextInput(attrs={"placeholder": "#으로 태그를 구분해서 입력하세요.", "id": "id_tag"})
    )
    
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
        
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['tags'] = self.clean_tag()
        return cleaned_data

# 포스트 이미지 생성 폼
# 미구현(사유: multiple 속성을 구현할 수 있는 방법이 없다.)
# class PostImageForm(forms.ModelForm):
#     image_url = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
#     class Meta:
#         model = PostImage
#         fields = ['image_url']
#         # widgets = {
#         #     'image_url': MultiFileField(),
#         # }
        
#     def clean(self):
        
#         return 

# 포스트 댓글 생성 폼
class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(attrs={"placeholder": "댓글을 입력하세요."}),
        }