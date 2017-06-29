from django import forms
from django.contrib.auth.models import User


class AuthorForm(forms.Form):
    username = forms.CharField(label = "username", max_length = 100)
    password = forms.CharField(label = "password", max_length = 100,widget=forms.PasswordInput(render_value=False))

class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    email = forms.CharField(label="email", max_length=100)
    first_name = forms.CharField(label = "first name", max_length = 100)
    last_name = forms.CharField(label = "last name", max_length = 100)
    password = forms.CharField(label="password", max_length=100,widget=forms.PasswordInput(render_value=False))