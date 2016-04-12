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
    template_name = 'alarms/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch alarms
        try:
            alarms = self.api.list_alarms(
                access_token=request.session['access_token']['access_token'],
                user_id=request.session['access_token']['user_id'],
            )

        # Fetching alarms failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Parse datetime strings
        for alarm in alarms['_embedded']['alarms']:
            alarm['created_at'] = parse_datetime(alarm['created_at'])
            alarm['updated_at'] = parse_datetime(alarm['updated_at'])

        return self._render(
            request=request,
            title='Alarms',
            active_link='alarms',
            alarms=alarms,
        )