from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse


class SignInView(View):
    initial = {}
    template_name = 'dashboard/sign-in.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            render(request, self.template_name, {
            'title': 'PINGLIST - Uptime And Performance Monitoring Done Right'}))
