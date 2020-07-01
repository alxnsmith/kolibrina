from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    format('%d-%m-%Y')


class EditUser(forms.Form):
    birthday = forms.DateField(widget=DateInput)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=(('Male', 'Мужской'), ('Female', 'Женский')))
    country = forms.ChoiceField(choices=(('RU', 'Россия'), ('UK', 'Украина'), ('BY', 'Беларусь'), ('KZ', 'Казахстан')))
    area = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Область проживания'}))
    city = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Город проживания'}))
    phoneNumber = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))

