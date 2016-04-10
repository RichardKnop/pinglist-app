import logging

from django.contrib import messages
from django.shortcuts import redirect
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
        # Initialise the form
        form = self.form_class(initial=self.initial)

        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Add a subscription
        try:
            self.api.add_subscription(
                access_token=request.session['access_token']['access_token'],
                plan_id=form.cleaned_data['plan'],
                card_id=form.cleaned_data['card'],
            )

            messages.success(request, 'Subscription added successfully')
            return redirect('subscriptions:index')

        # Adding subscription failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _short_plan_desc(self, plan):
        return '{} - ${}'.format(
            plan['name'],
            format(float(plan['amount']) / float(100), '.2f'),
        )

    def _short_card_desc(self, card):
        return '{} ending with {}'.format(
            card['brand'],
            card['last_four'],
        )

    def _render(self, request, form):
        # Fetch the plans
        plans = self.api.list_plans()

        # Fetch the cards
        cards = self.api.list_cards(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )

        # Load form select options
        form.fields['plan'].choices = (
            (p['id'], self._short_plan_desc(p))
            for p in plans['_embedded']['plans'])
        form.fields['payment_source'].choices = (
            (c['id'], self._short_card_desc(c))
            for c in cards['_embedded']['cards'])

        return super(AddView, self)._render(
            request=request,
            form=form,
            title='Add Subscription',
            active_link='subscriptions',
        )