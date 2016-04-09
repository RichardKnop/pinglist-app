import logging

from lib.auth import logged_in
from apps import BaseView


logger = logging.getLogger(__name__)


class MeView(BaseView):
    template_name = 'profile/me.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='My Profile',
            active_link='profile',
        )
