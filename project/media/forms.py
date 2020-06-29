from django import forms
from .models import Image


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'user')
        widgets = {'user': forms.HiddenInput()}
