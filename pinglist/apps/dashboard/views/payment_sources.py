import logging

from apps.api.decorators import logged_in

from apps import BaseView


logger = logging.getLogger(__name__)


class PaymentSourcesView(BaseView):
    template_name = 'dashboard/payment-sources.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Profile',
        )