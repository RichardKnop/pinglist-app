from django import forms


class LoginForm(forms.Form):

    email = forms.CharField(required=True)
    password = forms.CharField(required=True)