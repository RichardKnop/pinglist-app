from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from . import HTML_TITLE


class SubscriptionsView(View):
    initial = {}
    template_name = 'dashboard/subscriptions.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            render(request, self.template_name, {
            'title': HTML_TITLE}))
