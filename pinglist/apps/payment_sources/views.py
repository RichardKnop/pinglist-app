import logging

from lib.auth import logged_in
from apps import BaseView


logger = logging.getLogger(__name__)


class IndexView(BaseView):
    template_name = 'payment_sources/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        cards = self.api.list_cards(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )
        return self._render(
            request=request,
            title='Payment Sources',
            active_link='payment_sources',
            cards=cards,
        )


class AddView(BaseView):
    template_name = 'payment_sources/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Add Payment Source',
            active_link='payment_sources',
        )