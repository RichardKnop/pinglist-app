from django import forms
from django.core.validators import validate_email


class MultiEmailField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)


class TeamForm(forms.Form):

    name = forms.CharField(
        required=True,
        label='Name',
    )
    members = MultiEmailField(
        required=True,
        widget=forms.Textarea,
        label='Members (comma separated list of emails)',
    )


class AddForm(TeamForm):
    pass


class UpdateForm(TeamForm):
    pass


class DeleteForm(forms.Form):

    team_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput,
    )
