from django import forms
from django.core.validators import URLValidator


class AlarmForm(forms.Form):

    region = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        label='Region',
    )
    endpoint_url = forms.CharField(
        required=True,
        validators=[URLValidator(schemes=('http', 'https'))],
        label='Endpoint URL',
    )
    expected_http_code = forms.IntegerField(
        required=True,
        label='Expected HTTP Code',
    )
    max_response_time = forms.IntegerField(
        required=True,
        label='Max Response Time (ms)',
    )
    interval = forms.IntegerField(
        required=True,
        label='Interval (s)',
    )
    email_alerts = forms.BooleanField(
        required=False,
        label='Email Alerts',
    )
    push_notification_alerts = forms.BooleanField(
        required=False,
        label='Push Notification Alerts',
    )
    slack_alerts = forms.BooleanField(
        required=False,
        label='Slack Alerts',
    )
    active = forms.BooleanField(
        required=False,
        label='Active',
    )


class AddForm(AlarmForm):
    pass


class UpdateForm(AlarmForm):
    pass


class DeleteForm(forms.Form):

    alarm_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput,
    )
