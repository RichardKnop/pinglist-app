from django import forms


class SettingsForm(forms.Form):

    first_name = forms.CharField(
        required=True,
        max_length=100,
        label='First Name',
    )
    last_name = forms.CharField(
        required=True,
        max_length=100,
        label='Last Name',
    )
    slack_incoming_webhook = forms.CharField(
        required=False,
        max_length=200,
        label='Slack Incoming Webhook',
    )
    slack_channel = forms.CharField(
        required=False,
        max_length=100,
        label='Slack Channel (should start with #)',
    )


class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        required=False,
        label='Old Password (only needed when you already have a password)',
    )
    new_password = forms.CharField(
        required=True,
        min_length=6,
        label='New Password',
    )
    new_password_again = forms.CharField(
        required=True,
        min_length=6,
        label='New Password Again',
    )

