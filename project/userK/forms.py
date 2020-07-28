from django import forms


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
