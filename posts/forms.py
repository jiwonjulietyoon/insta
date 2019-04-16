from django import forms
from .models import Post, Comment

# Post라는 모델을 조작할 수 있는 PostModelForm 정의
class PostForm(forms.ModelForm):
    # 1. 어떤 input field를 가지는지
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={
        'placeholder': '오늘은 무엇을 하셨나요?'
    }))
    
    # 2. 해당 input field의 속성을 추가 & 어떤 모델을 조작할지
    class Meta:
        model = Post
        # fields = "__all__"
        fields = ['content', 'image']
        


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="댓글", widget=forms.TextInput(attrs={
        'placeholder': 'Comment'
        
    }))
    
    class Meta:
        model = Comment
        fields = ['content']
