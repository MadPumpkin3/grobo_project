from django import forms
from myapps.posts.models import Post, PostImage, PostComment
from myapps.form.custom_form import MultiFileField
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

# 중요: view에서 'PostCreateForm'과 'PostImageForm'이 하나의 폼처럼 나오게 작업해야함.
# 작업: PostImageFormset = formset_factory(PostImage, form=PostImageForm, extra=1)
# view에서 폼 생성시, 'PostCreateForm'를 먼저 호출하고, 그 뒤에 'PostImageFormset'를 호출해서 'form=PostImageForm'연결시키기

# 포스트 생성 폼
class PostCustomEditorForm(forms.Form):
    title = forms.CharField(
        label='제목', max_length=255, required=True, widget=forms.TextInput(attrs={"placeholder": "제목을 입력하세요.", "id": "post_title_id"})
    )
    content = MarkdownxFormField(
        label='내용', required=True, widget=MarkdownxWidget(attrs={"placeholder": "내용을 입력하세요.", "id": "post_markdown_id"})
    )
    tag = forms.CharField(
        label='태그', required=False, widget=forms.TextInput(attrs={"placeholder": "#으로 태그를 구분해서 입력하세요.", "id": "post_tag_id"})
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
            
            self.cleaned_data['tag'] = tags
            
        return self.cleaned_data['tag']
            
        
# 포스트 댓글 생성 폼
class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(attrs={"placeholder": "댓글을 입력하세요."}),
        }