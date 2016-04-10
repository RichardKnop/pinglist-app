import logging

from django.utils.dateparse import parse_datetime

from lib.auth import logged_in
from apps import BaseView
from apps.subscriptions.forms import AddForm


logger = logging.getLogger(__name__)


class IndexView(BaseView):
    template_name = 'subscriptions/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the subscriptions
        subscriptions = self.api.list_subscriptions(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )
        # Parse datetime strings
        for subscription in subscriptions['_embedded']['subscriptions']:
            subscription['started_at'] = parse_datetime(subscription['started_at'])
            subscription['cancelled_at'] = parse_datetime(subscription['cancelled_at'])
            subscription['ended_at'] = parse_datetime(subscription['ended_at'])
            subscription['period_start'] = parse_datetime(subscription['period_start'])
            subscription['period_end'] = parse_datetime(subscription['period_end'])

        return self._render(
            request=request,
            title='Subscriptions',
            active_link='subscriptions',
            subscriptions=subscriptions,
        )


class AddView(BaseView):
    form_class = AddForm
    template_name = 'subscriptions/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the plans
        plans = self.api.list_plans()

        form = self.form_class(initial=self.initial)

        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Log in with email and password
        try:
            print 'TODO'

        # Adding subscription failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        return super(AddView, self)._render(
            request=request,
            form=form,
            title='Add Subscription',
            active_link='subscriptions',
        )