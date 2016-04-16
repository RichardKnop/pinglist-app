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
