from django import forms


class TeamForm(forms.Form):

    name = forms.CharField(required=True, label='Name')


class AddForm(TeamForm):
    pass


class UpdateForm(TeamForm):
    pass


class DeleteForm(forms.Form):

    team_id = forms.CharField(required=True, widget=forms.HiddenInput)
