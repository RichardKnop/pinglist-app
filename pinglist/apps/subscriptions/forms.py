from django import forms


class AddForm(forms.Form):

    plan = forms.ChoiceField(required=True, widget=forms.Select)
    payment_source = forms.ChoiceField(required=True, widget=forms.Select)