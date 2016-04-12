from django import forms


class ProfileForm(forms.Form):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)