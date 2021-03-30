from django import forms

from user_profile.models import SignUpModel, SignInModel


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SignUpModel
        fields = ['username', 'email', 'password']


class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SignInModel
        fields = ['username', 'password']
