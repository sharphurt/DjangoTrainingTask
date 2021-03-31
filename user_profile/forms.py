from django import forms
from django.core.validators import RegexValidator

from user_profile.models import SignUpModel, SignInModel


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SignUpModel
        fields = ['username', 'email', 'password']


class SignInForm(forms.ModelForm):
    username = forms.CharField(min_length=1, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SignInModel
        fields = ['username', 'password']