from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'nickname',]


