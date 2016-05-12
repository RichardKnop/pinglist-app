from django import forms


class ProfileForm(forms.Form):

    first_name = forms.CharField(
        required=True,
        label='First Name',
    )
    last_name = forms.CharField(
        required=True,
        label='Last Name',
    )


class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        required=False,
        label='Old Password (only needed when you already have a password)',
    )
    new_password = forms.CharField(
        required=True,
        label='New Password',
    )
    new_password_again = forms.CharField(
        required=True,
        label='New Password Again',
    )

