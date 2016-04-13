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
from apps.alarms import AlarmView
from apps.alarms.forms import AddForm


logger = logging.getLogger(__name__)


class IndexView(AlarmView):
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


class AddView(AlarmView):
    form_class = AddForm
    template_name = 'alarms/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch regions
        regions = self.api.list_regions(
            access_token=request.session['access_token']['access_token'],
        )

        # Init the form
        form = self.form_class(initial=self.initial)
        self._set_form_choices(form=form, regions=regions)

        return self._render(
            request=request,
            form=form,
            regions=regions,
        )

    @logged_in
    def post(self, request, *args, **kwargs):
        # Fetch regions
        regions = self.api.list_regions(
            access_token=request.session['access_token']['access_token'],
        )

        # Init the form
        form = self.form_class(request.POST)
        self._set_form_choices(form=form, regions=regions)

        # Validate POST data
        if not form.is_valid():
            print form.errors
            return self._render(
                request=request,
                form=form,
                regions=regions,
            )

        # Add an alarm
        try:
            self.api.add_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm={
                    'region': form.cleaned_data['region'],
                    'endpoint_url': form.cleaned_data['endpoint_url'],
                    'expected_http_code': int(form.cleaned_data['expected_http_code']),
                    'max_response_time': int(form.cleaned_data['max_response_time']),
                    'interval': int(form.cleaned_data['interval']),
                    'email_alerts': True,
                    'push_notification_alerts': True if form.cleaned_data['push_notification_alerts'] else False,
                    'active': True if form.cleaned_data['active'] else False,
                },
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Alarm added successfully')
            return redirect('alarms:index')

        # Adding alarm failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                regions=regions,
            )

    def _render(self, request, form, regions):
        return super(AddView, self)._render(
            request=request,
            form=form,
            regions=regions,
            title='Add Alarm',
            active_link='alarms',
        )