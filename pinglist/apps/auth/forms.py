from django import forms


class RegisterForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Email',
    )
    password = forms.CharField(
        required=True,
        label='Password',
        min_length=6,
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


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label='Email',
    )
