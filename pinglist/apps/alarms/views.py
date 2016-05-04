import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import (
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.utils.dateparse import parse_datetime
from django.utils.timezone import datetime, timedelta

from lib.auth import logged_in
from apps import BaseView
from apps.alarms import AlarmView
from apps.alarms.forms import (
    AddForm,
    UpdateForm,
    DeleteForm,
)

logger = logging.getLogger('django')


class IndexView(AlarmView):
    template_name = 'alarms/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))

        # Fetch alarms
        try:
            alarms = self.api.list_alarms(
                access_token=request.session['access_token']['access_token'],
                user_id=request.session['access_token']['user_id'],
                page=page,
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
            page=page,
        )


class AddView(AlarmView):
    form_class = AddForm
    template_name = 'alarms/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch regions
        try:
            regions = self.api.list_regions(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching regions failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

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
        try:
            regions = self.api.list_regions(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching regions failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class(request.POST)
        self._set_form_choices(form=form, regions=regions)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                regions=regions,
            )

        # Add an alarm
        try:
            alarm = {
                'region': form.cleaned_data['region'],
                'endpoint_url': form.cleaned_data['endpoint_url'],
                'expected_http_code': int(form.cleaned_data['expected_http_code']),
                'max_response_time': int(form.cleaned_data['max_response_time']),
                'interval': int(form.cleaned_data['interval']),
                'email_alerts': form.cleaned_data['email_alerts'],
                'push_notification_alerts': form.cleaned_data['push_notification_alerts'],
                'active': form.cleaned_data['active'],
            }
            self.api.add_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm=alarm,
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


class UpdateView(AlarmView):
    form_class = UpdateForm
    template_name = 'alarms/update.html'

    @logged_in
    def get(self, request, alarm_id, *args, **kwargs):
        # Fetch regions
        try:
            regions = self.api.list_regions(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching regions failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Get the alarm
        try:
            alarm = self.api.get_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
            )

        # Alarm not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(initial={
            'region': alarm['region'],
            'endpoint_url': alarm['endpoint_url'],
            'expected_http_code': alarm['expected_http_code'],
            'max_response_time': alarm['max_response_time'],
            'interval': alarm['interval'],
            'email_alerts': alarm['email_alerts'],
            'push_notification_alerts': alarm['push_notification_alerts'],
            'active': alarm['active'],
        })
        self._set_form_choices(form=form, regions=regions)

        return self._render(
            request=request,
            form=form,
            regions=regions,
            alarm=alarm,
        )

    @logged_in
    def post(self, request, alarm_id, *args, **kwargs):
        # Fetch regions
        try:
            regions = self.api.list_regions(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching regions failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Get the alarm
        try:
            alarm = self.api.get_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
            )

        # Alarm not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(request.POST)
        self._set_form_choices(form=form, regions=regions)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                regions=regions,
                alarm=alarm,
            )

        # Update the alarm
        try:
            alarm['region'] = form.cleaned_data['region']
            alarm['endpoint_url'] = form.cleaned_data['endpoint_url']
            alarm['expected_http_code'] = int(form.cleaned_data['expected_http_code'])
            alarm['max_response_time'] = int(form.cleaned_data['max_response_time'])
            alarm['interval'] = int(form.cleaned_data['interval'])
            alarm['email_alerts'] = form.cleaned_data['email_alerts']
            alarm['push_notification_alerts'] = form.cleaned_data['push_notification_alerts']
            alarm['active'] = form.cleaned_data['active']
            self.api.update_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm=alarm,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Alarm updated successfully')
            return redirect('alarms:index')

        # Updating alarm failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                regions=regions,
                alarm=alarm,
            )

    def _render(self, request, form, regions, alarm):
        return super(UpdateView, self)._render(
            request=request,
            form=form,
            regions=regions,
            alarm=alarm,
            title='Update Alarm',
            active_link='alarms',
        )


class DeleteView(AlarmView):
    form_class = DeleteForm
    template_name = 'alarms/delete.html'

    @logged_in
    def get(self, request, alarm_id, *args, **kwargs):
        # Get the alarm
        try:
            alarm = self.api.get_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
            )

        # Alarm not found
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseNotFound()

        form = self.form_class(initial={'alarm_id': alarm_id})

        return self._render(
            request=request,
            form=form,
            alarm=alarm,
        )

    @logged_in
    def post(self, request, alarm_id, *args, **kwargs):
        # Get the alarm
        try:
            alarm = self.api.get_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
            )

        # Alarm not found
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
                alarm=alarm,
            )

        # Delete the alarm
        try:
            self.api.delete_alarm(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Alarm deleted successfully')
            return redirect('alarms:index')

        # Deleting alarm failed
        except self.api.APIError as e:
            logger.error(str(e))
            messages.error(request, str(e))
            return redirect('alarms:delete', alarm_id=alarm_id)

    def _render(self, request, form, alarm):
        return super(DeleteView, self)._render(
            request=request,
            form=form,
            alarm=alarm,
            title='Delete Alarm',
            active_link='alarms',
        )


class AlarmIncidentsView(BaseView):
    template_name = 'alarms/alarm-incidents.html'

    @logged_in
    def get(self, request, alarm_id, *args, **kwargs):
        page = int(request.GET.get('page', 1))

        # Fetch alarm incidents
        try:
            incidents = self.api.list_alarm_incidents(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
                page=page,
            )

        # Fetching alarm incidents failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Parse datetime strings
        for incident in incidents['_embedded']['incidents']:
            if incident['resolved_at']:
                incident['resolved_at'] = parse_datetime(incident['resolved_at'])
            incident['created_at'] = parse_datetime(incident['created_at'])
            incident['updated_at'] = parse_datetime(incident['updated_at'])

        return self._render(
            request=request,
            title='Alarm Incidents',
            active_link='alarms',
            alarm_id=alarm_id,
            incidents=incidents,
            page=page,
        )


class AlarmMetricsView(BaseView):
    template_name = 'alarms/alarm-metrics.html'

    @logged_in
    def get(self, request, alarm_id, *args, **kwargs):
        active_filter = request.GET.get('filter', '')
        today = datetime.today()
        metrics_params = {
            'last_hour': {
                'date_trunc': None,
                "date_from": today - timedelta(hours=1),
            },
            'last_day': {
                'date_trunc': 'hour',
                "date_from": today - timedelta(days=1),
            },
            'last_week': {
                'date_trunc': 'hour',
                "date_from": today - timedelta(days=7),
            },
            'last_month': {
                'date_trunc': 'day',
                "date_from": today - timedelta(days=30),
            },
        }

        # Fetch the alarm metrics
        try:
            metrics = self.api.list_alarm_metrics(
                access_token=request.session['access_token']['access_token'],
                alarm_id=alarm_id,
                date_trunc=metrics_params[active_filter]['date_trunc'],
                date_from=metrics_params[active_filter]['date_from'],
                date_to=None,
            )

        # Fetching alarm metrics failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()


        return self._render(
            request=request,
            title='Alarm Metrics',
            active_link='alarms',
            alarm_id=alarm_id,
            metrics=metrics,
            active_filter=active_filter,
        )
