from __future__ import absolute_import

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as django_settings

from lib.api import API


api_instance = API(
    django_settings.API_HOST,
    django_settings.OAUTH_CLIENT_ID,
    django_settings.OAUTH_CLIENT_SECRET,
    django_settings.OAUTH_DEFAULT_SCOPE,
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
            },
            'ios_link': django_settings.IOS_LINK,
            'is_development': django_settings.IS_DEVELOPMENT,
        }
        return HttpResponse(
            render(
                request,
                self.template_name,
                dict(data, **kwargs),
            )
        )
