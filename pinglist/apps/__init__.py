from __future__ import absolute_import

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from apps.api import API


API = API(
    settings.API_HOST,
    settings.OAUTH_CLIENT_ID,
    settings.OAUTH_CLIENT_SECRET,
    settings.OAUTH_DEFAULT_SCOPE,
)


class BaseView(View):
    initial = {}
    API = API

    def _render(self, request, **kwargs):
        data = {
            'logged_in': getattr(request, 'logged_in', False),
        }
        return HttpResponse(
            render(
                request,
                self.template_name,
                dict(data, **kwargs),
            )
        )