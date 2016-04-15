from __future__ import absolute_import

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from lib.api import API


api_instance = API(
    settings.API_HOST,
    settings.OAUTH_CLIENT_ID,
    settings.OAUTH_CLIENT_SECRET,
    settings.OAUTH_DEFAULT_SCOPE,
)


class BaseView(View):
    initial = {}
    api = api_instance

    def _render(self, request, **kwargs):
        data = {
            'error': getattr(request, 'error', None),
            'logged_in': getattr(request, 'logged_in', False),
            'request_path': request.path,
            'message_type_to_alert_class': {
                'debug': 'info',
                'info': 'info',
                'success': 'success',
                'warning': 'warning',
                'error': 'danger',
            }
        }
        return HttpResponse(
            render(
                request,
                self.template_name,
                dict(data, **kwargs),
            )
        )
