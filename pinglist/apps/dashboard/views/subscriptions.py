import logging

from lib.auth import logged_in
from apps import BaseView


logger = logging.getLogger(__name__)


class SubscriptionsView(BaseView):
    template_name = 'dashboard/subscriptions.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        subscriptions = self.api.list_subscriptions(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )
        return self._render(
            request=request,
            title='Subscriptions',
            active_link='subscriptions',
            subscriptions=subscriptions,
        )


class AddSubscriptionView(BaseView):
    template_name = 'dashboard/add_subscription.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Add Subscription',
            active_link='subscriptions',
        )