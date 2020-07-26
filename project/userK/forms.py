from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    format('%d-%m-%Y')


class EditUser(forms.Form):
    birthday = forms.DateField(widget=DateInput)
    league = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        (0, 'Школьная лига / Лига колледжей'), (1000, 'Студенческая лига'), (3000, 'Высшая лига'),
        (6000, 'Премьер-лига'), (10000, 'Супер-лига'),
    ))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=(('Male', 'Мужской'), ('Female', 'Женский')))
    country = forms.ChoiceField(choices=(('RU', 'Россия'), ('UK', 'Украина'), ('BY', 'Беларусь'), ('KZ', 'Казахстан')))
    area = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Регион'}))
    city = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Город'}))
    phoneNumber = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))

