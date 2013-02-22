
from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=20, initial='user')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    host = forms.IPAddressField(initial='127.0.0.1')  # could be ipv4 for the moment.
    port = forms.IntegerField(min_value=1001, max_value=65535, initial=7022)


class SearchForm(forms.Form):
    terms = forms.CharField(max_length=256, initial='terms')
#    file_type = forms.CharField(max_length=20, initial='media')
#    max_results = forms.IntegerField(min_value=10, max_value=10000, initial=500)
#    min_filesize = forms.IntegerField(min_value=0, max_value=10000, initial=0)
#    max_filesize = forms.IntegerField(min_value=1, max_value=10000, initial=10000)


class ChatForm(forms.Form):
    message = forms.CharField(max_length=1000)

