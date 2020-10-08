from django import forms
from django.contrib.auth.forms import UserCreationForm
from userK.models import User


class RegForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', )
    error_messages = {
        'password_mismatch': 'Пароли не совпали!',
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_active')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        for user in User.objects.filter(email=email):
            if user.is_active:
                raise forms.ValidationError(u'Пользователь с таким e-mail уже зарегестрирован.')
            elif user is not None:
                User.objects.filter(email=email)[0].delete()
        return email
