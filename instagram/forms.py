from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        widgets = {
            # Char 로 범위가 지정되어 보여서, 늘리기위해, 폼 혐태를 변경함
            "caption": forms.Textarea
        }


