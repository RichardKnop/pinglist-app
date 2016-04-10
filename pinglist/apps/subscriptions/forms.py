from django import forms


class AddForm(forms.Form):

    plan = forms.ChoiceField(required=True, widget=forms.Select)
    payment_source = forms.ChoiceField(required=True, widget=forms.Select)


class UpdateForm(forms.Form):

    plan = forms.ChoiceField(required=True, widget=forms.Select)
    payment_source = forms.ChoiceField(required=True, widget=forms.Select)


class CancelForm(forms.Form):

    subscription_id = forms.CharField(required=True, widget=forms.HiddenInput)