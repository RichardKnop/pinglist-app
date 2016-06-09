from django import forms


class PasswordForm(forms.Form):

    password = forms.CharField(
        required=True,
        label='Password',
        min_length=6,
    )
    password_again = forms.CharField(
        required=True,
        label='Confirm Password',
        min_length=6,
    )


class ConfirmInvitationForm(PasswordForm):
    pass


class ConfirmPasswordResetForm(PasswordForm):
    pass
