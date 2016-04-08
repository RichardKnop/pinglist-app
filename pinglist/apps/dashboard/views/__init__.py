from __future__ import absolute_import

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from .. import API


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


def get_facebook_redirect_uri():
    return '{}{}'.format(
        settings.HOSTNAME,
        reverse('dashboard:facebook_redirect'),
    )

def get_facebook_authorize_uri():
    return 'https://www.facebook.com/dialog/oauth?client_id={}&scope={}&redirect_uri={}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SCOPE,
        get_facebook_redirect_uri(),
    )
