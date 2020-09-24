from django import forms
from .models import Question


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('author', 'category', 'theme', 'difficulty', 'question', 'correct_answer',
                  'answer2', 'answer3', 'answer4')
        widgets = {'difficulty': forms.RadioSelect,
                   'author': forms.HiddenInput}

