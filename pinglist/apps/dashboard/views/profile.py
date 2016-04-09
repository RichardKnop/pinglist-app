import logging

from lib.auth import logged_in
from apps import BaseView


logger = logging.getLogger(__name__)


class ProfileView(BaseView):
    template_name = 'dashboard/profile.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        return self._render(
            request=request,
            title='Profile',
            active_link='profile',
        )
