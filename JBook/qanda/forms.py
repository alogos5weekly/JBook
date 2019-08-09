from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_title', 'question_text', )
