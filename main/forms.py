from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, PasswordInput, EmailInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        # widgets = {
        #     "username":TextInput(
        #         attrs={
        #             'class':'form-control',
        #             'placeholder':'Username'
        #         }
        #     ),
        #     "password":PasswordInput(
        #         attrs={
        #             'class':'form-control'
        #         }
        #     ),
        #     "email":EmailInput(
        #         attrs={
        #             'class':'form-control'
        #         }
        #     )
        # }

class LoginForm(AuthenticationForm):
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    #     widgets = {
    #         "username":TextInput(
    #             attrs={
    #                 'class':'form-control'
    #             }
    #         ),
    #         "password": PasswordInput(
    #             attrs={
    #                 'class': 'form-control'
    #             }
    #         )
    #     }
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control'}))