from django import forms
from django.conf import settings
from django.utils import timezone

from userK.models import User


class RegistrationForm(forms.Form):
    base_classes = 'string'
    widgets = {
        'username_input': forms.TextInput({
            'class': base_classes,
            'placeholder': 'Username',
            'pattern': '[a-zA-Z\d_]*',
            'title': 'Только латинские символы, цифры и "_"'
        }),
        'birthday_input': forms.DateInput({
            'class': base_classes,
            'placeholder': 'День рождения',
            'onfocus': "this.type = 'date'",
            'min': (timezone.now() - timezone.timedelta(days=365.25 * 100)).date(),
            'max': (timezone.now() - timezone.timedelta(days=365.25 * 14)).date()
        }),
        'email_input': forms.EmailInput({
            'class': base_classes,
            'placeholder': 'E-Mail',
            'max-length': 200,
        }),
        'password1_input': forms.PasswordInput({
            'class': base_classes,
            'placeholder': 'Пароль',
        }),
        'password2_input': forms.PasswordInput({
            'class': base_classes,
            'placeholder': 'Повторите пароль',
        }),
    }
    username = forms.CharField(widget=widgets['username_input'])
    birthday = forms.DateField(widget=widgets['birthday_input'])
    email = forms.CharField(widget=widgets['email_input'])
    password1 = forms.CharField(widget=widgets['password1_input'])
    password2 = forms.CharField(widget=widgets['password2_input'])

    def clean_username(self):
        username = self.cleaned_data.get('username', False).lower().strip()
        for word in settings.RESERVED_USERNAME_WORDS:
            if word in username:
                msg = 'В имени пользователя используются зарезервированые ключевые слова: ' + word
                raise forms.ValidationError(msg)
        if User.objects.filter(username=username).exists():
            msg = ['Username занят']
            raise forms.ValidationError(msg)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if User.objects.filter(email=email).exists():
            msg = ['E-Mail занят.']
            raise forms.ValidationError(msg)
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday', False)
        years_old = (timezone.now().date() - birthday).days / 365.25
        if years_old < 14.00:
            msg = ['К самостоятельной регистрации допускаются лица достигшие 14 лет. ',
                   'Для регистрации обратитесь к родителю.']
            raise forms.ValidationError(msg)
        return birthday

    def clean(self):
        password1 = self.cleaned_data.get('password1', False)
        password2 = self.cleaned_data.get('password2', False)
        if not password1:
            self.add_error('password1')
        elif not password2:
            self.add_error('password2')
        elif password1 != password2:
            msg = ['Пароли не совпадают']
            self.add_error('password1')
            self.add_error('password2', msg)

    def add_error(self, field, msg=None):
        if msg is None:
            msg = ''
        super(RegistrationForm, self).add_error(field, msg)
        self.fields[field].widget.attrs['class'] += ' error'


class DateInput(forms.DateInput):
    input_type = 'date'
    format('%d-%m-%Y')


class EditUser(forms.Form):
    birthday = forms.DateField(widget=DateInput)
    league = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('l1', 'Школьная лига'), ('l2', 'Лига колледжей'), ('l3', 'Студенческая лига'),
        ('l4', 'Высшая лига'), ('l5', 'Премьер-лига'), ('l6', 'Супер-лига'))
                               )
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=(('Male', 'Мужской'), ('Female', 'Женский')))
    country = forms.ChoiceField(choices=(('RU', 'Россия'), ('UK', 'Украина'), ('BY', 'Беларусь'), ('KZ', 'Казахстан')))
    area = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Регион'}))
    city = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Город'}))
    phoneNumber = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
