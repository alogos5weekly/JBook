from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
    (False, 'No'),
    (True, 'Yes')
)

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail',
        'categories', 'is_anonymous')


    is_anonymous = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select())

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )
