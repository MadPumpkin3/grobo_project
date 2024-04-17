from django import forms
from myapps.feeds.models import Feed, FeedImage, FeedComment
from myapps.form.custom_form import MultiFileField

# 피드 업로드 필드
class FeedCreateForm(forms.ModelForm):
    
    class Meta:
        model = Feed
        fields = ['context', 'tag']
        widgets = {
            'context': forms.Textarea(attrs={'placeholder': '내용을 입력해주세요.'}),
            'tag': forms.CharField(widget=forms.TextInput(attrs={'placeholder': '#으로 태그를 구분하여 입력해주세요.'})),
        }
        
    def clean_tag(self):
        tag_data = self.cleaned_data['tag']
        
        if tag_data:
            tags = [tag.strip() for tag in tag_data.split('#') if tag.strip()]
            return tags

# 이미지 업로드 필드        
class FeedImageForm(forms.Form):
    image_url = MultiFileField(label="이미지", required=False,
                               # ClearableFileInput : 파일 입력 필드에 파일을 선택하거나 현재 선택된 파일을 지울 수 있는 클리어 버튼을 제공
                               widget=(forms.ClearableFileInput(attrs={'placeholder':'선택사항입니다.', 'multiple':True})))

# 댓글 업로드 필드    
class FeedCommentForm(forms.ModelForm):
    
    class Meta:
        model = FeedComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder':'댓글을 입력해주세요.'})
        }