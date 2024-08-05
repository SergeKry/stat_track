from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Form for user registration"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'username',
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'password',
        'class': 'form-control',
        'placeholder': 'Create password',
        'type': 'password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'password',
        'class': 'form-control',
        'placeholder': 'Confirm password',
        'type': 'password',
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    """Form for login"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'username',
        'class': 'form-control',
        'placeholder': 'Username',
        "autofocus": True
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'password',
        'class': 'form-control',
        'placeholder': 'Password',
    }))
