from django import forms


class RegisterForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Email',
    )
    password = forms.CharField(
        required=True,
        label='Password',
    )


class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Email',
    )
    password = forms.CharField(
        required=True,
        label='Password',
    )