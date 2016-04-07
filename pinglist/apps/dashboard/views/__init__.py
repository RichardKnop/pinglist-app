from __future__ import absolute_import

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from .. import API


class BaseView(View):
    initial = {}
    API = API
    HTML_TITLE = 'PINGLIST - Uptime And Performance Monitoring Done Right'

    def _render(self, request, **kwargs):
        data = {
            'title': self.HTML_TITLE,
            'logged_in': getattr(request, 'logged_in', False),
        }
        return HttpResponse(
            render(
                request,
                self.template_name,
                dict(data, **kwargs),
            )
        )
