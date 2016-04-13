from django import forms


class AlarmForm(forms.Form):

    region = forms.ChoiceField(required=True, widget=forms.Select)
    endpoint_url = forms.CharField(required=True)
    expected_http_code = forms.CharField(required=True)
    max_response_time = forms.CharField(required=True)
    interval = forms.CharField(required=True)
    email_alerts = forms.BooleanField(required=False)
    push_notification_alerts = forms.BooleanField(required=False)
    active = forms.BooleanField(required=False)


class AddForm(AlarmForm):
    pass


class UpdateForm(AlarmForm):
    pass


class DeleteForm(forms.Form):

    alarm_id = forms.CharField(required=True, widget=forms.HiddenInput)