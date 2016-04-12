from django import forms


class SubscriptionForm(forms.Form):

    plan = forms.ChoiceField(required=True, widget=forms.Select)


class AddForm(SubscriptionForm):
    pass


class UpdateForm(SubscriptionForm):
    pass


class CancelForm(forms.Form):

    subscription_id = forms.CharField(required=True, widget=forms.HiddenInput)