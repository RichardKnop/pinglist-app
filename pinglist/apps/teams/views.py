import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import (
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

from lib.auth import logged_in
from apps import BaseView
from apps.teams.forms import (
    AddForm,
    UpdateForm,
    DeleteForm,
)


logger = logging.getLogger(__name__)


class IndexView(BaseView):
    template_name = 'teams/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch teams
        try:
            teams = self.api.list_teams(
                access_token=request.session['access_token']['access_token'],
                user_id=request.session['access_token']['user_id'],
            )

        # Fetching teams failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Parse datetime strings
        for team in teams['_embedded']['teams']:
            team['created_at'] = parse_datetime(team['created_at'])
            team['updated_at'] = parse_datetime(team['updated_at'])

        return self._render(
            request=request,
            title='Teams',
            active_link='teams',
            teams=teams,
        )


class AddView(BaseView):
    form_class = AddForm
    template_name = 'teams/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(
            request=request,
            form=form,
        )

    @logged_in
    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
            )

        # Add a team
        try:
            team = {
                'name': form.cleaned_data['name'],
            }
            self.api.add_team(
                access_token=request.session['access_token']['access_token'],
                team=team,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Team added successfully')
            return redirect('teams:index')

        # Adding team failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
            )

    def _render(self, request, form):
        return super(AddView, self)._render(
            request=request,
            form=form,
            title='Add Team',
            active_link='teams',
        )


class UpdateView(BaseView):
    form_class = UpdateForm
    template_name = 'teams/update.html'

    @logged_in
    def get(self, request, team_id, *args, **kwargs):
        # Get the team
        try:
            team = self.api.get_team(
                access_token=request.session['access_token']['access_token'],
                team_id=team_id,
            )

        # Team not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(initial={
            'name': team['name'],
        })

        return self._render(
            request=request,
            form=form,
            team=team,
        )

    @logged_in
    def post(self, request, team_id, *args, **kwargs):
        # Get the team
        try:
            team = self.api.get_team(
                access_token=request.session['access_token']['access_token'],
                team_id=team_id,
            )

        # Team not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                team=team,
            )

        # Update the team
        try:
            team['name'] = form.cleaned_data['name']
            self.api.update_team(
                access_token=request.session['access_token']['access_token'],
                team=team,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Team updated successfully')
            return redirect('teams:index')

        # Updating team failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                team=team,
            )

    def _render(self, request, form, team):
        return super(UpdateView, self)._render(
            request=request,
            form=form,
            team=team,
            title='Update Team',
            active_link='teams',
        )


class DeleteView(BaseView):
    form_class = DeleteForm
    template_name = 'teams/delete.html'

    @logged_in
    def get(self, request, team_id, *args, **kwargs):
        # Get the team
        try:
            team = self.api.get_team(
                access_token=request.session['access_token']['access_token'],
                team_id=team_id,
            )

        # Team not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        form = self.form_class(initial={'team_id': team_id})

        return self._render(
            request=request,
            form=form,
            team=team,
        )

    @logged_in
    def post(self, request, team_id, *args, **kwargs):
        # Get the team
        try:
            team = self.api.get_team(
                access_token=request.session['access_token']['access_token'],
                team_id=team_id,
            )

        # Team not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                team=team,
            )

        # Delete the team
        try:
            self.api.delete_team(
                access_token=request.session['access_token']['access_token'],
                team_id=team_id,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Team deleted successfully')
            return redirect('teams:index')

        # Deleting team failed
        except self.api.APIError as e:
            logger.error(str(e))
            messages.error(request, str(e))
            return redirect('teams:delete', team_id=team_id)

    def _render(self, request, form, team):
        return super(DeleteView, self)._render(
            request=request,
            form=form,
            team=team,
            title='Delete Team',
            active_link='teams',
        )
