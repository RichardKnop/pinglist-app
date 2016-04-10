from django import forms


class AddCardForm(forms.Form):

    stripe_token = forms.CharField(required=True)


class DeleteCardForm(forms.Form):

    card_id = forms.CharField(required=True, widget=forms.HiddenInput)