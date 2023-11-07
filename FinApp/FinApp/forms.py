from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('password')


    First_Name = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'firstName',
        }
    ))

    Last_Name = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'lastName',
        }
    ))

    Email = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'email',
        }
    ))

    Password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ))