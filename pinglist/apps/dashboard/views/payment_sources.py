import logging

from lib.auth import logged_in
from apps import BaseView


logger = logging.getLogger(__name__)


class PaymentSourcesView(BaseView):
    template_name = 'dashboard/payment-sources.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Payment Sources',
            active_link='payment_sources',
        )
