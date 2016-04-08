from django.shortcuts import redirect
from django.conf import settings

from apps import BaseView


class LogoutView(BaseView):

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect(settings.LOGIN_VIEW)