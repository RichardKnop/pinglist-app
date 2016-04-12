import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import (
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.utils.dateparse import parse_datetime

from lib.auth import logged_in
from apps import BaseView


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