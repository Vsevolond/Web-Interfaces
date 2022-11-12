from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(label='user_login', max_length=100)
    password = forms.CharField(label='user_password', max_length=100)