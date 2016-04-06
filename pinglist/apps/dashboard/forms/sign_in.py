from django import forms


class SignInForm(forms.Form):

    email = forms.CharField(required=True)
    password = forms.CharField(required=True)