from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    firstName = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'firstName',
        }
    ))

    lastName = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'lastName',
        }
    ))

    email = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'email',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ))