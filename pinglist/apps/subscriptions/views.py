import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.utils.dateparse import parse_datetime

from lib.auth import logged_in
from . import SubscriptionView
from apps.subscriptions.forms import (
    AddForm,
    UpdateForm,
    CancelForm,
)


logger = logging.getLogger(__name__)


class IndexView(SubscriptionView):
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
            subscription['trial_start'] = parse_datetime(subscription['trial_start'])
            subscription['trial_end'] = parse_datetime(subscription['trial_end'])

        return self._render(
            request=request,
            title='Subscriptions',
            active_link='subscriptions',
            subscriptions=subscriptions,
        )


class AddView(SubscriptionView):
    form_class = AddForm
    template_name = 'subscriptions/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)
        self._set_form_choices(request=request, form=form)

        return self._render(request=request, form=form)

    @logged_in
    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)
        self._set_form_choices(request=request, form=form)

        # Validate POST data
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Add a subscription
        try:
            self.api.add_subscription(
                access_token=request.session['access_token']['access_token'],
                plan_id=int(form.cleaned_data['plan']),
                card_id=int(form.cleaned_data['payment_source']),
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Subscription added successfully')
            return redirect('subscriptions:index')

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

class UpdateView(SubscriptionView):
    form_class = UpdateForm
    template_name = 'subscriptions/update.html'

    @logged_in
    def get(self, request, subscription_id, *args, **kwargs):
        # Get the subscription
        try:
            subscription = self.api.get_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=subscription_id,
            )

        # Card not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(initial=self.initial)
        self._set_form_choices(request=request, form=form)

        return self._render(
            request=request,
            form=form,
            subscription=subscription,
        )

    @logged_in
    def post(self, request, subscription_id, *args, **kwargs):
        # Get the subscription
        try:
            subscription = self.api.get_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=subscription_id,
            )

        # Card not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(request.POST)
        self._set_form_choices(request=request, form=form)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                subscription=subscription,
            )

        # Update the subscription
        try:
            self.api.update_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=int(subscription_id),
                plan_id=int(form.cleaned_data['plan']),
                card_id=int(form.cleaned_data['payment_source']),
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Subscription updated successfully')
            return redirect('subscriptions:index')

        # Adding subscription failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                subscription=subscription,
            )

    def _render(self, request, form, subscription):
        return super(UpdateView, self)._render(
            request=request,
            form=form,
            subscription=subscription,
            title='Update Subscription',
            active_link='subscriptions',
        )

class CancelView(SubscriptionView):
    form_class = CancelForm
    template_name = 'subscriptions/cancel.html'

    @logged_in
    def get(self, request, subscription_id, *args, **kwargs):
        # Get the subscription
        try:
            subscription = self.api.get_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=subscription_id,
            )

        # Subscription not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        form = self.form_class(initial={'subscription_id': subscription_id})

        return self._render(
            request=request,
            form=form,
            subscription=subscription,
        )

    @logged_in
    def post(self, request, subscription_id, *args, **kwargs):
        # Get the subscription
        try:
            subscription = self.api.get_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=subscription_id,
            )

        # Subscription not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                subscription=subscription,
            )

        # Cancel the subscription
        try:
            self.api.cancel_subscription(
                access_token=request.session['access_token']['access_token'],
                subscription_id=subscription_id,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Subscription cancelled successfully')
            return redirect('subscriptions:index')

        # Cancelling subscription failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                subscription=subscription,
            )

    def _render(self, request, form, subscription):
        return super(CancelView, self)._render(
            request=request,
            form=form,
            subscription=subscription,
            title='Cancel Subscription',
            active_link='subscriptions',
        )