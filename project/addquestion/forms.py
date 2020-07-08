from django import forms
from .models import Questions


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('author', 'category', 'theme', 'difficulty', 'question', 'corectAnsw', 'answer2', 'answer3', 'answer4')
        widgets = {'difficulty': forms.RadioSelect, 'author': forms.HiddenInput}

