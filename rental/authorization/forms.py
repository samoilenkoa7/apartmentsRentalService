from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class-name': 'form-field'
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class-name': 'form-field'
    }))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={
        'class-name': 'form-field'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class-name': 'form-field'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomLoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class-name': 'form-field'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class-name': 'form-field'
    }))
