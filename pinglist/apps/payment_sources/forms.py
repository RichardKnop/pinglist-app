from django import forms


class AddForm(forms.Form):

    stripe_token = forms.CharField(required=True)


class DeleteForm(forms.Form):

    card_id = forms.CharField(required=True, widget=forms.HiddenInput)