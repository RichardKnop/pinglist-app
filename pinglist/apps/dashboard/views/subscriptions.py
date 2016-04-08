import logging

from apps.api.decorators import logged_in

from apps import BaseView


logger = logging.getLogger(__name__)


class SubscriptionsView(BaseView):
    template_name = 'dashboard/subscriptions.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Subscriptions',
        )
