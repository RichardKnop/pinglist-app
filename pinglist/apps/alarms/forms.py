from django import forms


class AlarmForm(forms.Form):

    region = forms.ChoiceField(required=True, widget=forms.Select, label='Region')
    endpoint_url = forms.CharField(required=True, label='Endpoint URL')
    expected_http_code = forms.CharField(required=True, label='Expected HTTP Code')
    max_response_time = forms.CharField(required=True, label='Max Response Time (ms)')
    interval = forms.CharField(required=True, label='Interval (s)')
    email_alerts = forms.BooleanField(required=False, label='Email Alerts')
    push_notification_alerts = forms.BooleanField(required=False, label='Push Notification Alerts')
    active = forms.BooleanField(required=False, label='Active')


class AddForm(AlarmForm):
    pass


class UpdateForm(AlarmForm):
    pass


class DeleteForm(forms.Form):

    alarm_id = forms.CharField(required=True, widget=forms.HiddenInput)
